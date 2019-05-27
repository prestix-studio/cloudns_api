# -*- coding: utf-8 -*-
#
# name:             api.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       09/15/2018
#

"""
cloudns_api.api
~~~~~~~~~~~~~~~

This module contains basic API utilities and the api decorator function.
"""

from json import dumps as to_json_string
from requests import codes as code, get, post
from requests.exceptions import ContentDecodingError, ConnectionError
from requests.exceptions import HTTPError, SSLError, TooManyRedirects
from requests.exceptions import ConnectTimeout, Timeout, ReadTimeout

from .config import (
    CLOUDNS_API_AUTH_ID,
    CLOUDNS_API_AUTH_PASSWORD,
    CLOUDNS_API_DEBUG,
)
from .validation import ValidationError


def get_auth_params():
    """Returns a dict pre-populated with auth parameters."""
    return {'auth-id': CLOUDNS_API_AUTH_ID,
            'auth-password': CLOUDNS_API_AUTH_PASSWORD}


def api(api_call):
    """ Decorates an api call in order to consistently handle errors and
    maintain a consistent json format.

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

            print('Set as:')
            print(CLOUDNS_API_DEBUG)

            if CLOUDNS_API_DEBUG:
                print('soo.. debugging.')
                result['error'] = e.__str__()
            else:
                result['error'] = 'Something went wrong.'


        # Whew! Made it past the errors, so return the result
        if 'json_object' in kwargs and kwargs['json_object']:
            return result

        return to_json_string(result)

    return api_wrapper


@api
def get_login():
    """Returns the login status using available credentials."""
    return get('https://api.cloudns.net/dns/login.json',
               params=get_auth_params())


@api
def get_nameservers():
    """Returns the available nameservers."""
    return get('https://api.cloudns.net/dns/available-name-servers.json',
               params=get_auth_params())
