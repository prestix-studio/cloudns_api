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

from json import loads as load_as_json
from os import environ
from requests import codes as code, get, post


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


class ValidationError(Exception):
    """Exception thrown when a validation error has occured."""


def api(api_call):
    """ Decorates an api call in order to consistently handle errors and maintain a
    consistent json format.
    """

    def api_wrapper(*args, **kwargs):
        """ Wraps an api call in order to consistently handle errors and
        maintain a consistent json format.

        :param json_object: bool, return an object if true, otherwise return
            the json string
        """
        try:
            result = api_call(*args, **kwargs)
            data_object = load_as_json(result.text)

            # Check for HTTP error codes
            if result.status_code is not code.OK:
                json_string = '{"success":false, "status_code":' + status_code \
                    + ', data":' + result.text + '}'

            # Check for API error codes
            elif 'status' in data_object and data_object['status'] == 'Failed':
                json_string = '{"success":false, "error":"' + \
                    data_object['statusDescription'] + '", "data":' + result.text \
                    + '}'

            # Otherwise, just format using our json
            else:
                json_string = '{"success":true, "data":' + result.text + '}'

        # Catch Validation errors
        except ValidationError as e:
            json_string = '{"success":false, "error":"Validation error."}'
            pass

        # Catch Other Python errors
        except TypeError as e:
            print(e)
            json_string = '{"success":false, "error":"Missing argument."}'

        if 'json_object' in kwargs and kwargs['json_object']:
            return load_as_json(json_string)

        return json_string

    return api_wrapper
