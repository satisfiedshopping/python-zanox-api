# encoding: utf-8

import datetime
import hmac
import hashlib
import base64
import random
import string
import json
from urlparse import urlparse

from urllib import urlencode

import requests
import xmltodict


def random_string(length, characters=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    return ''.join(random.choice(characters) for character in range(length))


class PublisherApi(object):

    def __init__(self, connect_id, secret_key, domain='api.zanox.com', format='json', version='2011-03-01', ssl=True, *args, **kwargs):
        self.connect_id = connect_id
        self.secret_key = secret_key
        self.ssl = ssl
        self.protocol = 'https' if self.ssl else 'http'
        self.domain = domain
        self.version = version
        self.format = format
        self.datetime_format = '%a, %d %b %Y %H:%M:%S GMT' # example: Thu, 15 Aug 2013 15:56:07 GMT
        self.session = None

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

    @staticmethod
    def extract_destination_url_from_tracking_url(tracking_url, clean=False):
        response = requests.head(tracking_url, allow_redirects=True)
        if clean:
            url_parts = urlparse(response.url)
            destination_url = '{0}://{1}{2}'.format(url_parts.scheme, url_parts.netloc, url_parts.path)
        else:
            destination_url = response.url
        return destination_url

    def get_signature(self, url, method, date, nonce):
        # construct signature
        uri = self.extract_uri_from_url(url)
        date = date.strftime(self.datetime_format)
        method = method.upper()
        elements = (method, uri, date, nonce)
        signature = u''.join(elements)

        # encode signature SHA256, and Base 64
        signature = hmac.new(self.secret_key, msg=signature, digestmod=hashlib.sha1).digest()
        signature = base64.b64encode(signature)
        signature = '%s:%s' % (self.connect_id, signature)
        return signature

    def get_request_headers(self, url, method):
        # format datetime
        date = datetime.datetime.utcnow()
        nonce = random_string(32)
        signature = self.get_signature(url, 'GET', date, nonce)
        headers = {
            'Authorization': "ZXWS {0}".format(signature),
            'Date': date.strftime(self.datetime_format),
            'nonce': nonce,
        }
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
        headers = self.get_request_headers(url, method='GET')
        response = requests.get(url, headers=headers)
        json = response.json()
        return json

    def get_program_identifier(self, tracking_url):
        return tracking_url.lower().split('&ulp')[0].split('ppc/?')[1]

    def get_tracking_url(self, destination_url, adspace_id):
        """Get a tracking url for a given destination url and adspace id"""
        deeplink_api_url = '{0}://toolbox.zanox.com/tools/api/deeplink?connectid={1}&adspaceid={2}&url={3}'.format(self.protocol, self.connect_id, adspace_id, destination_url)
        response = requests.get(deeplink_api_url)
        tracking_url = xmltodict.parse(response.text)['deeplink']['url']
        return tracking_url

    def put(self, content, path, query=None):
        return