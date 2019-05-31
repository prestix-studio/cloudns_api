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


class ApiResponse(object):
    def __init__(self, response=None):
        """Wrapper object to add custom functionality and properties to a
        request response object.

        :param response: requests.models.response, Requests response object.
        """
        self.error = None
        self.validation_errors = None

        if response:
            self.create(response)
        else:
            self.response = None

    def create(self, response):
        """Creates the the response and checks for HTTP and API errors.

        :param response: requests.models.response, Requests response object.
        """
        self.response = response

        # Check for HTTP error codes
        if self.status_code is not code.OK:
            self.error = 'HTTP response ' + self.status_code

        # Check for API error responses
        elif 'status' in self.data and self.data['status'] is 'Failed':
            self.error = self.data['statusDescription']

    @property
    def success(self):
        """Returns the success status of the response. Successful when the
        status_code is ok and there are no error messages."""
        return self.status_code is code.OK and not self.error

    @property
    def status_code(self):
        """Wraps the request response's status code."""
        return self.response.status_code if self.response else None

    @property
    def data(self):
        """Wraps the request response's json method."""
        return self.response.json() if self.response else {}

    def json(self):
        """Returns the response as a json object."""
        json = {
            'status_code' : self.status_code,
            'sucess'      : self.success,
            'data'        : self.data,
        }

        if self.error:
            json['error'] = self.error

        if self.validation_errors:
            json['validation_errors'] = self.validation_errors

        if CLOUDNS_API_DEBUG and not self.success and not self.error:
            json['error'] = 'Response has not yet been created with a requests.response.'

        return json

    def string(self):
        """Returns the json response as a string."""
        return to_json_string(self.json())


def api(api_call):
    """Decorates an api call in order to consistently handle errors and
    maintain a consistent json format.

    :param api_call: function, the function to be decorated
    """

    def api_wrapper(*args, **kwargs):
        """ Wraps an api call in order to consistently handle errors and
        maintain a consistent json format.

        :param json_object: bool, return an object if true, otherwise return
            the json string
        """
        response = ApiResponse()

        try:
            response.create(api_call(*args, **kwargs))

        # Catch Timeout errors
        except (ConnectTimeout, Timeout, ReadTimeout) as e:
            response.error = 'API Connection timed out.'

        # Catch Connection errors
        except (ContentDecodingError, ConnectionError, HTTPError, SSLError,
                TooManyRedirects) as e:
            response.error = 'API Network Connection error.'

        # Catch Validation errors
        except ValidationError as e:
            response.error = 'Validation error.'
            response.validation_errors = e.get_details()

        # Catch Other Python errors
        except TypeError as e:
            response.error = 'Missing a required argument.'

        # Catch all other python errors
        except Exception as e:
            response.error = 'Something went wrong.'

            if CLOUDNS_API_DEBUG:
                response.error = e.__str__()


        # Whew! Made it past the errors, so return the result
        if 'json_object' in kwargs and kwargs['json_object']:
            return response.json()


        return response.string()

    return api_wrapper


def patch_update(get, keys):
    """Decorates an api call to allow 'patch' updating with only parameters to
    be updated.

    :param api_call: function, the function to be decorated
    """

    def decorated_patch_update(api_call):
        """Decorates an api call to allow 'patch' updating with only parameters to
        be updated.

        :param api_call: function, the function to be decorated
        """

        def api_wrapper(patch=False, *args, **kwargs):
            """ Wraps an api call in order to allow 'patching'
            maintain a consistent json format.

            :param patch: bool, retrieve current parameter values to pass with the
                parameters given. If False, does nothing. False by default.
            """
            if patch:
                result = get(json_object=True, **{key:value for key,value in
                                                  kwargs.items() if key in
                                                  keys})
                if not result['success']:
                    raise Exception('fix this...')

                kwargs = {**result['data'], **kwargs}

            return api_call(*args, **kwargs)

        return api_wrapper

    return decorated_patch_update


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
