#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             test_api.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       09/16/2018
#

"""
Functional tests for cloudns-api's api utilities module.
"""


from os import environ
from pytest import fixture
from requests import exceptions as request_exceptions


# Set environment vars to test vars
environ['CLOUDNS_AUTH_ID'] = 'user_id_123'
environ['CLOUDNS_AUTH_PASSWORD'] = 'user_password_123'
orig_clouds_auth_id = environ.get('CLOUDNS_AUTH_ID')
orig_clouds_auth_password = environ.get('CLOUDNS_AUTH_PASSWORD')

# Import only after changing environment variables to test vars
from cloudns_api import api
from cloudns_api.validation import ValidationError

# Reset environment variables to original state
environ['CLOUDNS_AUTH_ID'] = orig_clouds_auth_id
environ['CLOUDNS_AUTH_PASSWORD'] = orig_clouds_auth_password


##
# Authentication Tests

def test_get_auth_params_returns_auth_params_from_environment():
    """Function get_auth_params should return auth as set in environment."""
    auth_params = api.get_auth_params()
    assert auth_params['auth-id'] == 'user_id_123'
    assert auth_params['auth-password'] == 'user_password_123'


def test_get_auth_params_returns_different_dict_every_time():
    """Function get_auth_params returns a different dict that is not modified
    from previous operations."""
    auth_params = api.get_auth_params()
    auth_params['a-param'] = 'a-value'
    assert 'a-param' in auth_params

    new_params = api.get_auth_params()
    assert 'a-param' not in new_params


##
# API Decorator Tests

class MockResponse:
    """Mocks a response from the requests library."""
    def __init__(self, json_data = None, status_code = 200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mock_response(*args, **kwargs):
    """Mocks requests.get or requests.post for tests."""
    return MockResponse({"key1": "value1"}, 200)


def test_api_decorator_returns_string_by_default():
    """Decorator 'api' returns the result as a string by default."""

    @api.api
    def test_api_call(*args, **kwargs):
        return MockResponse(json_data = {'response': 'Testing...'})

    result = test_api_call()
    assert '{"response": "Testing..."}' in result


def test_api_decorator_can_return_object():
    """Decorator 'api' can return an object from JSON."""

    @api.api
    def test_api_call(*args, **kwargs):
        return MockResponse(json_data = {'response': 'Testing...'})

    result = test_api_call(json_object = True)
    assert result['data']['response'] == 'Testing...'


def test_api_decorator_responds_to_success():
    """API decorator responds appropriately to successful requests."""

    @api.api
    def test_api_call(*args, **kwargs):
        return MockResponse(json_data = {'response': 'Testing...'})

    result = test_api_call(json_object = True)
    assert result['success'] is True


def test_api_decorator_responds_to_network_errors():
    """API decorator responds appropriately to network errors."""

    @api.api
    def test_api_call(*args, **kwargs):
        raise request_exceptions.ConnectionError()

    result = test_api_call(json_object = True)
    assert result['success'] is False
    assert result['error'] == 'API Network Connection error.'


def test_api_decorator_responds_to_timeout_errors():
    """API decorator responds appropriately to network timeout errors."""

    @api.api
    def test_api_call(*args, **kwargs):
        raise request_exceptions.ConnectTimeout()

    result = test_api_call(json_object = True)
    assert result['success'] is False
    assert result['error'] == 'API Connection timed out.'


def test_api_decorator_responds_to_500_errors():
    """API decorator responds appropriately to non-200 status codes."""

    @api.api
    def test_api_call(*args, **kwargs):
        return MockResponse(json_data = {'response': 'Testing...'},
                            status_code = 500)

    result = test_api_call(json_object = True)
    assert result['success'] is False
    assert result['status_code'] == 500


def test_api_decorator_responds_to_bad_python_code():
    """API decorator responds appropriately to bad python code."""

    @api.api
    def test_api_call(*args, **kwargs):
        return bad_python_code

    result = test_api_call(json_object = True)
    assert result['success'] is False
    assert result['error'] == 'Something went wrong.'


def test_api_decorator_responds_to_missing_required_args():
    """API decorator responds appropriately to required missing args."""

    @api.api
    def test_api_call(required_arg, *args, **kwargs):
        return bad_python_code

    result = test_api_call(json_object = True)
    assert result['success'] is False
    assert result['error'] == 'Missing a required argument.'


def test_api_decorator_responds_to_validation_error():
    """API decorator responds appropriately to validation error."""

    @api.api
    def test_api_call(*args, **kwargs):
        raise ValidationError('the_field_name',
                                  'The field should be in this format.')

    result = test_api_call(json_object = True)
    assert result['success'] is False
    assert result['error'] == 'Validation error.'
    assert result['validation_error']['field'] == 'the_field_name'
    assert result['validation_error']['message'] == 'The field should be in this format.'


def test_api_decorator_responds_to_authentication_error():
    """API decorator responds appropriately to authentication error."""

    @api.api
    def test_api_call(*args, **kwargs):
        return MockResponse(json_data = {'status': 'Failed',
                                         'statusDescription':
                                         'Invalid authentication, incorrect auth-id or auth-password.'})

    result = test_api_call(json_object = True)
    assert result['success'] is False
    assert result['error'] == 'Invalid authentication, incorrect auth-id or auth-password.'
