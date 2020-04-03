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
from re import compile as re_compile
import requests
from requests import codes as code
from requests.exceptions import (
    ContentDecodingError,
    ConnectionError,
    HTTPError,
    SSLError,
    TooManyRedirects,
    ConnectTimeout,
    Timeout,
    ReadTimeout,
)

from .config import (
    CLOUDNS_API_AUTH_ID,
    CLOUDNS_API_AUTH_PASSWORD,
    CLOUDNS_API_DEBUG,
    CLOUDNS_API_SUB_AUTH_ID,
    CLOUDNS_API_SUB_AUTH_USER,
    CLOUDNS_API_TESTING,
)
from .validation import ValidationError


def get_auth_params():
    """Returns a dict pre-populated with auth parameters."""
    # Get password parameter
    if not CLOUDNS_API_TESTING and not CLOUDNS_API_AUTH_PASSWORD:  # pragma: no cover
        raise EnvironmentError(
            'Environment variable "CLOUDNS_API_AUTH_PASSWORD" not set.'
        )
    auth_params = {'auth-password': CLOUDNS_API_AUTH_PASSWORD}

    # Get username parameter
    if CLOUDNS_API_AUTH_ID:
        auth_params['auth-id'] = CLOUDNS_API_AUTH_ID
    elif CLOUDNS_API_SUB_AUTH_ID:
        auth_params['sub-auth-id'] = CLOUDNS_API_SUB_AUTH_ID
    elif CLOUDNS_API_SUB_AUTH_USER:
        auth_params['sub-auth-user'] = CLOUDNS_API_SUB_AUTH_USER
    elif not CLOUDNS_API_TESTING:  # pragma: no cover
        raise EnvironmentError(
            'No environment variable "CLOUDNS_API_AUTH_ID", '
            '"CLOUDNS_API_SUB_AUTH_ID" or "CLOUDNS_API_SUB_AUTH_USER" is set.'
        )

    return auth_params


_first_cap_re = re_compile('(.)([A-Z][a-z]+)')
_all_cap_re = re_compile('([a-z0-9])([A-Z])')


def convert_to_snake_case(string):
    string = str(string)
    string = _first_cap_re.sub(r'\1_\2', string)
    string = _all_cap_re.sub(r'\1_\2', string).lower()
    return string


def use_snake_case_keys(original_dict):
    """Converts a dict's keys to snake case.

    @see https://stackoverflow.com/questions/1175208
    """
    normalized_dict = {}

    for key, value in original_dict.items():
        normalized_dict[convert_to_snake_case(key)] = value

    return normalized_dict


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

    def __str__(self):
        """Returns the string value of the response."""
        return self.string()

    def create(self, response):
        """Creates the the response and checks for HTTP and API errors.

        :param response: requests.models.response, Requests response object.
        """
        self.response = response

        try:
            self.error = self.payload['error']
        except (TypeError, KeyError):
            pass

        # Check for HTTP error codes
        if not self.error and self.status_code is not code.OK:
            self.error = 'HTTP response ' + str(self.status_code)

        # Check for error responses from ClouDNS
        elif isinstance(self.payload, dict) \
                and 'status' in self.payload \
                and self.payload['status'] == 'Failed':
            self.error = self.payload['status_description']

    @property
    def success(self):
        """Returns the success status of the response. Successful when the
        status_code is ok and there are no error messages."""
        return self.status_code is code.OK and not self.error

    @property
    def status_code(self):
        """Wraps the request response's status code."""
        if hasattr(self, '_status_code'):
            return self._status_code
        return self.response.status_code if self.response else None

    @status_code.setter
    def status_code(self, status_code):
        """Status code setter"""
        self._status_code = status_code

    @property
    def payload(self):
        """Wraps the request response's json method."""
        if not self.response:
            return {}

        payload = self.response.json()  # Get the requests response json

        if isinstance(payload, dict):
            return use_snake_case_keys(payload)
        else:
            return payload

    def json(self):
        """Returns the response as a json object. This allows us to scrub the
        payload and massage it to our requirements."""
        json = {
            'status_code':  self.status_code,
            'success':      self.success,
            'payload':      self.payload,
        }

        if self.error:
            json['error'] = self.error

        if self.validation_errors:
            json['validation_errors'] = self.validation_errors

        if CLOUDNS_API_DEBUG and not self.success and not self.error:
            json['error'] = \
                'Response has not yet been created with a requests.response.'

        return json

    def string(self):
        """Returns the json response as a json string."""
        return to_json_string(self.json())


class RequestResponseStub(object):
    def __init__(self, payload=None, status_code=200):
        """Requests response stub used for stubbing request responses in the
        API code as well as for testing for testing.

        :param payload: dict, json data to be returned in the json() method.
        :param status_code: integer, the status code to return in the test.
            Defaults to 200.
        """
        self.payload = payload if payload else {}
        self.status_code = status_code

    def json(self):
        """Mocks the json object method."""
        return self.payload


class ApiException(Exception):
    status_code = code.BAD_REQUEST

    def __init__(self, message, *args, **kwargs):
        """An exception type reported and caught by the API.

        :param message: string a message to report to the user.
        """
        self.message = message
        super(ApiException, self).__init__(*args, **kwargs)


def api(api_call):
    """Decorates an api call in order to consistently handle errors and
    maintain a consistent json format.

    The decorated function should return a requests.response (or
    RequestResponseStub), and this wrapper will cause the function to finally
    return an ApiResponse.

    :param api_call: function, the function to be decorated
    """

    def api_wrapper(*args, **kwargs):
        """ Wraps an api call in order to consistently handle errors and
        maintain a consistent json format.
        """
        response = ApiResponse()

        try:
            response.create(api_call(*args, **kwargs))

        # Catch Timeout errors
        except (ConnectTimeout, Timeout, ReadTimeout) as e:
            response.error = 'API Connection timed out.'
            response.status_code = code.GATEWAY_TIMEOUT

            if CLOUDNS_API_DEBUG:  # pragma: no cover
                response.error = str(e)

        # Catch Connection errors
        except (ContentDecodingError, ConnectionError, HTTPError, SSLError,
                TooManyRedirects) as e:
            response.error = 'API Network Connection error.'
            response.status_code = code.SERVER_ERROR

            if CLOUDNS_API_DEBUG:  # pragma: no cover
                response.error = str(e)

        # Catch API reported exceptions
        except ApiException as e:
            response.error = e.message
            response.status_code = e.status_code

        # Catch Validation errors
        except ValidationError as e:
            response.error = 'Validation error.'
            response.validation_errors = e.get_details()
            response.status_code = code.BAD_REQUEST

        # Catch all other errors
        except Exception as e:
            response.error = 'Something went wrong.'
            response.status_code = code.SERVER_ERROR

            if CLOUDNS_API_DEBUG:
                response.error = str(e)

            if CLOUDNS_API_TESTING:
                import traceback
                print('\n' + traceback.format_exc())

        # Whew! Made it past the errors, so return the response
        return response

    return api_wrapper


def patch_update(get, keys):
    """Decorates an api call to allow 'patch' updating with only parameters to
    be updated.

    :param get: function, the function that should be used to get the existing
        parameters.
    :param keys: list, the list of keys that will be passed in the kwargs that
        should be used to get the existing data.
    """

    def decorated_patch_update(api_call):
        """Decorates an api call to allow 'patch' updating with only parameters to
        be updated.

        :param api_call: function, the function to be decorated
        """

        def api_wrapper(*args, **kwargs):
            """ Wraps an api call in order to allow 'patching'
            maintain a consistent json format.

            :param patch: bool, retrieve current parameter values to pass with
                the parameters given. If False, does nothing. False by default.
            """
            if 'patch' in kwargs and kwargs['patch']:
                response = get(*args, **{key: value for key, value in
                                         kwargs.items() if key in keys})
                if not response.success:
                    # Return the requests.response. The API decorator will
                    # return the original response.
                    return response

                kwargs = {**response.payload, **kwargs}

            return api_call(*args, **kwargs)

        return api_wrapper

    return decorated_patch_update


@api
def get_login():
    """Returns the login status using available credentials."""
    return requests.get('https://api.cloudns.net/dns/login.json',
                        params=get_auth_params())


@api
def get_nameservers():
    """Returns the available nameservers."""
    return requests.get(
        'https://api.cloudns.net/dns/available-name-servers.json',
        params=get_auth_params())


@api
def get_my_ip():
    """Returns the caller's ip address.

    NOTE: This doesn't seem to be working on ClouDNS's servers.
    """
    return requests.get('https://api.cloudns.net/dns/get-my-ip.json',
                        params=get_auth_params())
