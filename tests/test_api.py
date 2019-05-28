#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             test_api.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       09/16/2018
#

"""
Functional tests for cloudns_api's api utilities module.
"""

from os import environ
from requests import exceptions as request_exceptions

from cloudns_api.api import api, get_auth_params
from cloudns_api.validation import ValidationError

from .helpers import set_debug, set_no_debug, use_test_auth


##
# Authentication Tests

@use_test_auth
def test_get_auth_params_returns_auth_params(test_id, test_password):
    auth_params = get_auth_params()
    assert auth_params['auth-id'] == test_id
    assert auth_params['auth-password'] == test_password


def test_get_auth_params_returns_different_dict_every_time():
    """Function get_auth_params returns a different dict that is not modified
    from previous operations."""
    auth_params = get_auth_params()
    auth_params['a-param'] = 'a-value'
    assert 'a-param' in auth_params

    new_params = get_auth_params()
    assert 'a-param' not in new_params


##
# API Decorator Tests

# Utilities

class MockResponse:
    """Mocks a response from the requests library."""
    def __init__(self, json_data = None, status_code = 200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


# Tests

def test_api_decorator_returns_string_by_default():
    """Decorator 'api' returns the result as a string by default."""

    @api
    def test_api_call(*args, **kwargs):
        return MockResponse(json_data = {'response': 'Testing...'})

    result = test_api_call()
    assert '{"response": "Testing..."}' in result


def test_api_decorator_can_return_object():
    """Decorator 'api' can return an object from JSON."""

    @api
    def test_api_call(*args, **kwargs):
        return MockResponse(json_data = {'response': 'Testing...'})

    result = test_api_call(json_object = True)
    assert result['data']['response'] == 'Testing...'


def test_api_decorator_responds_to_success():
    """API decorator responds appropriately to successful requests."""

    @api
    def test_api_call(*args, **kwargs):
        return MockResponse(json_data = {'response': 'Testing...'})

    result = test_api_call(json_object = True)
    assert result['success'] is True


def test_api_decorator_responds_to_network_errors():
    """API decorator responds appropriately to network errors."""

    @api
    def test_api_call(*args, **kwargs):
        raise request_exceptions.ConnectionError()

    result = test_api_call(json_object = True)
    assert result['success'] is False
    assert result['error'] == 'API Network Connection error.'


def test_api_decorator_responds_to_timeout_errors():
    """API decorator responds appropriately to network timeout errors."""

    @api
    def test_api_call(*args, **kwargs):
        raise request_exceptions.ConnectTimeout()

    result = test_api_call(json_object = True)
    assert result['success'] is False
    assert result['error'] == 'API Connection timed out.'


def test_api_decorator_responds_to_500_errors():
    """API decorator responds appropriately to non-200 status codes."""

    @api
    def test_api_call(*args, **kwargs):
        return MockResponse(json_data = {'response': 'Testing...'},
                            status_code = 500)

    result = test_api_call(json_object = True)
    assert result['success'] is False
    assert result['status_code'] == 500


@set_no_debug
def test_api_decorator_responds_to_bad_python_code():
    """API decorator responds appropriately to bad python code."""

    @api
    def test_api_call(*args, **kwargs):
        # Bad python code:
        return uninitialized_variable

    result = test_api_call(json_object = True)
    assert result['success'] is False
    assert result['error'] == 'Something went wrong.'


@set_debug
def test_api_decorator_responds_specifically_to_bad_code_when_debugging():
    """API decorator responds more specifically to bad python code when in
    debug mode."""

    @api
    def test_api_call(*args, **kwargs):
        # Bad python code:
        return uninitialized_variable

    ## NEED TO turn off debug for this.

    result = test_api_call(json_object = True)
    assert result['success'] is False
    assert result['error'] == "name 'uninitialized_variable' is not defined"


def test_api_decorator_responds_to_missing_required_args():
    """API decorator responds appropriately to required missing args."""

    @api
    def test_api_call(required_arg, *args, **kwargs):
        return bad_python_code

    result = test_api_call(json_object = True)
    assert result['success'] is False
    assert result['error'] == 'Missing a required argument.'


def test_api_decorator_responds_to_validation_error():
    """API decorator responds appropriately to validation error."""

    @api
    def test_api_call(*args, **kwargs):
        raise ValidationError('the_field_name',
                                  'The field should be in this format.')

    result = test_api_call(json_object = True)
    assert result['success'] is False
    assert result['error'] == 'Validation error.'
    assert result['validation_errors'][0]['fieldname'] == 'the_field_name'
    assert result['validation_errors'][0]['message'] == 'The field should be in this format.'


def test_api_decorator_responds_to_authentication_error():
    """API decorator responds appropriately to authentication error."""

    @api
    def test_api_call(*args, **kwargs):
        return MockResponse(json_data = {'status': 'Failed',
                                         'statusDescription':
                                         'Invalid authentication, incorrect auth-id or auth-password.'})

    result = test_api_call(json_object = True)
    assert result['success'] is False
    assert result['error'] == 'Invalid authentication, incorrect auth-id or auth-password.'
