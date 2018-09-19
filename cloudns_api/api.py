#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             api.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       09/15/2018
#

"""
clouddns.api
~~~~~~~~~~~~

This module contains API utilities and preliminary parameters data structure.
"""

from __future__ import absolute_import

from .validation import ValidationError
from json import dumps as to_json_string
from os import environ
from requests import codes as code, get, post
from requests.exceptions import ContentDecodingError, ConnectionError
from requests.exceptions import HTTPError, SSLError, TooManyRedirects
from requests.exceptions import ConnectTimeout, Timeout, ReadTimeout


API_AUTH_ID = environ.get('CLOUDNS_AUTH_ID')
if not API_AUTH_ID:
    raise EnvironmentError('Environment variable "CLOUDNS_AUTH_ID" not set.')

API_AUTH_PASSWORD = environ.get('CLOUDNS_AUTH_PASSWORD')
if not API_AUTH_PASSWORD:
    raise EnvironmentError('Environment variable "CLOUDNS_AUTH_PASSWORD" not set.')

RECORD_TYPES = ['A', 'AAAA', 'MX', 'CNAME', 'TXT', 'NS', 'SRV', 'WR',
                'RP', 'SSHFP', 'ALIAS', 'CAA', 'PTR' ]


def get_auth_params():
    """Returns a dict pre-populated with auth parameters."""
    return {'auth-id': API_AUTH_ID,
            'auth-password': API_AUTH_PASSWORD}


def api(api_call):
    """ Decorates an api call in order to consistently handle errors and maintain a
    consistent json format.

    :param api_call: function, the function to be decorated
    """

    def api_wrapper(*args, **kwargs):
        """ Wraps an api call in order to consistently handle errors and
        maintain a consistent json format.

        :param json_object: bool, return an object if true, otherwise return
            the json string
        """
        result = {}

        try:
            response = api_call(*args, **kwargs)
            result['data'] = response.json()

            # Check for HTTP error codes
            if response.status_code is not code.OK:
                result['success'] = False
                result['status_code'] = response.status_code
                result['error'] = 'HTTP response ' + response.status_code

            # Check for API error responses
            elif 'status' in result['data'] and result['data']['status'] == 'Failed':
                result['success'] = False
                result['error'] = result['data']['statusDescription']

            # Otherwise, we're good
            else:
                result['success'] = True

        # Catch Timeout errors
        except (ConnectTimeout, Timeout, ReadTimeout) as e:
            result['success'] = False
            result['error'] = 'API Connection timed out.'

        # Catch Connection errors
        except (ContentDecodingError, ConnectionError, HTTPError, SSLError,
                TooManyRedirects) as e:
            result['success'] = False
            result['error'] = 'API Network Connection error.'

        # Catch Validation errors
        except ValidationError as e:
            result['success'] = False
            result['error'] = 'Validation error.'
            result['validation_errors'] = e.get_details()

        # Catch Other Python errors
        except TypeError as e:
            result['success'] = False
            result['error'] = 'Missing a required argument.'

        # Catch all other python errors
        except Exception as e:
            result['success'] = False
            result['error'] = 'Something went wrong.'


        # Whew! Made it past the errors, so return the result
        if 'json_object' in kwargs and kwargs['json_object']:
            return result

        return to_json_string(result)

    return api_wrapper


@api
def get_login():
    """Returns the login status using available credentials."""
    params = get_auth_params()
    params['auth-id'] = '12'
    return get('https://api.cloudns.net/dns/login.json',
               params=params)
    return get('https://api.cloudns.net/dns/login.json',
               params=get_auth_params())


@api
def get_nameservers():
    """Returns the available nameservers."""
    return get('https://api.cloudns.net/dns/available-name-servers.json',
               params=get_auth_params())
