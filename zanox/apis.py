# encoding: utf-8

import datetime
import hmac
import hashlib
import base64
import random
import string
import json

from urlparse import urlparse, parse_qs
from urllib import urlencode

from zanox import __version__

import requests
import xmltodict


class PublisherApi(object):

    def __init__(self, connect_id, secret_key, domain='api.zanox.com', format='json', version='2011-03-01', ssl=True, user_agent=None, from_email=None, *args, **kwargs):
        self.connect_id = connect_id
        self.secret_key = secret_key
        self.ssl = ssl
        self.protocol = 'https' if self.ssl else 'http'
        self.domain = domain
        self.version = version
        self.format = format
        self.datetime_format = '%a, %d %b %Y %H:%M:%S GMT' # example: Thu, 15 Aug 2013 15:56:07 GMT
        self.session = None
        self.user_agent = user_agent or "PythonZanoxApi/{0}".format(__version__)
        self.from_email = from_email
        self.tracking_url_format = 'http://ad.zanox.com/ppc/?{tracking_id}&ULP=[[{destination}]]&zpar9=[[{connect_id}]]'

        # Go through keyword arguments, and either save their values to the instance
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def construct_url(self, resource, format=None, **parameters):
        # construct url
        url_kwargs = {
            'protocol': self.protocol,
            'domain': self.domain,
            'format': format or self.format,
            'version': self.version,
            'resource': resource.strip('/'),
        }
        url = '{protocol}://{domain}/{format}/{version}/{resource}'.format(**url_kwargs)
        if parameters:
            url = '?'.join((url, urlencode(parameters)))
        return url

    def extract_uri_from_url(self, url):
        url_parts = urlparse(url)
        uri = url_parts.path.split(self.version)[-1]
        return uri

    def extract_destination_url_from_tracking_url(self, tracking_url, clean=False):
        headers = self.get_default_headers()
        response = requests.head(tracking_url, allow_redirects=True, headers=headers)

        # Adfarm has jasvascript/html redirecting and returns 200 status code
        # Let's extract the real destination url from de url
        destination_url = response.url
        if 'adfarm.mediaplex.com' in response.url:
            query = urlparse(destination_url).query
            destination_url = query.split('mpro=')[-1]

        # Strip the query parameters full of tracking stuff
        if clean:
            url_parts = urlparse(destination_url)
            destination_url = '{0}://{1}{2}'.format(url_parts.scheme, url_parts.netloc, url_parts.path)
        return destination_url

    def get_signature(self, url, method, date, nonce):
        # Construct signature
        uri = self.extract_uri_from_url(url)
        date = date.strftime(self.datetime_format)
        method = method.upper()
        elements = (method, uri, date, nonce)
        signature = u''.join(elements)

        # Encode signature SHA256, and Base64
        signature = hmac.new(self.secret_key, msg=signature, digestmod=hashlib.sha1).digest()
        signature = base64.b64encode(signature)
        signature = '%s:%s' % (self.connect_id, signature)
        return signature

    def get_default_headers(self):
        headers = {'User-Agent': self.user_agent}
        if self.from_email:
            headers['From'] = self.from_email
        return headers

    @staticmethod
    def generate_nonce(length=32, characters=string.ascii_uppercase + string.ascii_lowercase + string.digits):
        return ''.join(random.choice(characters) for item in range(length))

    def get_authenticated_headers(self, url, method):
        # format datetime
        date = datetime.datetime.utcnow()
        nonce = self.generate_nonce()
        signature = self.get_signature(url, 'GET', date, nonce)
        headers = dict(self.get_default_headers())
        headers.update({
            'Authorization': "ZXWS {0}".format(signature),
            'Date': date.strftime(self.datetime_format),
            'nonce': nonce,
        })
        return headers

    @staticmethod
    def get_page_numbers(json):
        number_of_pages = int(json['total'] / json['items'])
        page_numbers = range(number_of_pages)
        return page_numbers

    def pretty_print(self, json_object):
        print json.dumps(json_object, indent=4, sort_keys=True)

    def get(self, resource, **parameters):
        url = self.construct_url(resource, **parameters)
        headers = self.get_authenticated_headers(url, method='GET')
        response = requests.get(url, headers=headers)
        if self.format == 'json':
            return response.json()
        return response

    def get_program_identifier(self, tracking_url):
        return tracking_url.lower().split('&ulp')[0].split('ppc/?')[1]

    def get_tracking_url(self, destination_url, adspace_id=None, tracking_id=None, use_deeplink_generator=True):
        """Get a tracking url for a given destination url and adspace id"""

        if use_deeplink_generator:
            # Generate the link with de API
            if not adspace_id:
                raise Exception("`adspace_id` is required when you use the deeplink generator")
            deeplink_api_url = '{0}://toolbox.zanox.com/tools/api/deeplink?connectid={1}&adspaceid={2}&url={3}'.format(self.protocol, self.connect_id, adspace_id, destination_url)
            headers = self.get_default_headers()
            response = requests.get(deeplink_api_url, headers=headers)
            print response.text
            tracking_url = xmltodict.parse(response.text)['deeplink']['url']
        else:
            # Generate the link with the given trakcing url format
            if not tracking_id:
                raise Exception("`tracking_id` is required when you use the deeplink generator")
            tracking_url_parameters = {
                'tracking_id': tracking_id,
                'connect_id': self.connect_id,
                'destination': destination_url
            }
            tracking_url = self.tracking_url_format.format(**tracking_url_parameters)
        return tracking_url

    def put(self, content, path, query=None):
        return