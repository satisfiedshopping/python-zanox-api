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

    def get_page_numbers(self, json):
        number_of_pages = int(json['total'] / json['items'])
        page_numbers = range(number_of_pages)
        return page_numbers

    def pretty_print(self, json_object):
        print json.dumps(json_object, indent=4, sort_keys=True)

    def get(self, resource, **parameters):
        url = self.construct_url(resource, **parameters)
        print "GET {0}".format(url)
        headers = self.get_request_headers(url, method='GET')
        response = requests.get(url, headers=headers)
        json = response.json()
        return json

    def get_program_identifier(self, tracking_url):
        return tracking_url.lower().split('&ulp')[0].split('ppc/?')[1]

    def get_tracking_url(self, destination_url, adspace):
        """Get a tracking url for a given destination url and adspace id"""

        # authenticate
        if not self.session:
            self.session = requests.session()
            login_form_data = {
                'loginForm.loginViaUserAndPassword': True,
                'loginForm.userName': self.username,
                'loginForm.password': self.password,
            }
            self.session.post('https://auth.zanox.com/connect/login?appid=A5B83584B42A666E5309', data=login_form_data)

        # submit deeplink form and extract the tracking url
        deeplink_form_data = {
            'network': 'zanox',
            'url': destination_url,
            'zanox_adspaces': adspace,
        }
        response = self.session.post('http://toolbox.zanox.com/deeplink/', data=deeplink_form_data)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(response.content)
        try:
            tracking_url = soup.find(id='result_url')['value']
        except:
            return None
        return tracking_url

    def put(self, content, path, query=None):
        return