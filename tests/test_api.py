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

from requests import exceptions as request_exceptions

from cloudns_api.api import ApiResponse, api, get_auth_params, patch_update
from cloudns_api.validation import ValidationError

from .helpers import set_debug, set_no_debug, use_test_auth


##
# Authentication Tests


# Utilities

class MockRequestResponse:
    """Mocks a response from the requests library."""
    def __init__(self, json_data = None, status_code = 200):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


# Tests

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
#  Tests ApiResponse

def test_api_response_can_be_initialized_with_request_response():
    """An ApiResponse object can be initialized with a request response object.
    """
    request_response = MockRequestResponse(json_data={'test': 123}, status_code=200)
    response = ApiResponse(request_response)

    assert not response.error
    assert response.response == request_response
    assert response.success
    assert response.status_code is 200
    assert response.data == {'test' : 123}
    assert response.json() == {
            'status_code' : 200,
            'success'      : True,
            'data' : {'test' : 123}
        }


@set_no_debug
def test_api_response_can_be_initialized_without_request_response():
    """An ApiResponse object can be initialized without a request response
    object."""
    response = ApiResponse()

    assert not response.error
    assert not response.response
    assert not response.success
    assert not response.status_code
    assert response.data == {}
    assert response.json() == {
            'status_code' : None,
            'success'      : False,
            'data'        : {}
        }


@set_debug
def test_api_response_without_request_response_shows_error_in_json_when_debugging():
    """An ApiResponse object that is initialized without a request response
    object shows an error in the json when debugging."""
    response = ApiResponse()

    assert response.json()['error'] == 'Response has not yet been created with a requests.response.'


def test_api_response_can_have_error_set_on_response_without_request_response():
    """An ApiResponse object can have an error set on a response that has been
    initilized without a request response."""
    response = ApiResponse()

    response.error = 'Test error'

    assert response.error == 'Test error'
    assert response.response == None
    assert not response.success
    assert not response.status_code
    assert response.data == {}


def test_api_response_can_be_created_with_request_response_after_init():
    request_response = MockRequestResponse(json_data={'test': 123}, status_code=200)
    response = ApiResponse()
    response.create(request_response)

    assert not response.error
    assert response.response == request_response
    assert response.success
    assert response.status_code == 200
    assert response.data == {'test': 123}
    assert response.json() == {
            'status_code' : 200,
            'success'      : True,
            'data'        : {'test': 123}
        }


##
# API Decorator Tests


def test_api_decorator_returns_string_by_default():
    """Decorator 'api' returns the result as a string by default."""

    @api
    def test_api_call(*args, **kwargs):
        return MockRequestResponse(json_data = {'response': 'Testing...'})

    result = test_api_call()
    assert '{"response": "Testing..."}' in result


def test_api_decorator_can_return_object():
    """Decorator 'api' can return an object from JSON."""

    @api
    def test_api_call(*args, **kwargs):
        return MockRequestResponse(json_data = {'response': 'Testing...'})

    result = test_api_call(json_object = True)
    assert result['data']['response'] == 'Testing...'


def test_api_decorator_responds_to_success():
    """API decorator responds appropriately to successful requests."""

    @api
    def test_api_call(*args, **kwargs):
        return MockRequestResponse(json_data = {'response': 'Testing...'})

    result = test_api_call(json_object = True)
    assert result['success']


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
    assert not result['success']
    assert result['error'] == 'API Connection timed out.'


def test_api_decorator_responds_to_500_errors():
    """API decorator responds appropriately to non-200 status codes."""

    @api
    def test_api_call(*args, **kwargs):
        return MockRequestResponse(json_data = {'response': 'Testing...'},
                                   status_code = 500)

    result = test_api_call(json_object = True)
    assert not result['success']
    assert result['status_code'] == 500


@set_no_debug
def test_api_decorator_responds_to_bad_python_code():
    """API decorator responds appropriately to bad python code."""

    @api
    def test_api_call(*args, **kwargs):
        # Bad python code:
        return uninitialized_variable

    result = test_api_call(json_object = True)
    assert not result['success']
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
    assert not result['success']
    assert result['error'] == "name 'uninitialized_variable' is not defined"


def test_api_decorator_responds_to_missing_required_args():
    """API decorator responds appropriately to required missing args."""

    @api
    def test_api_call(required_arg, *args, **kwargs):
        return bad_python_code

    result = test_api_call(json_object = True)
    assert not result['success']
    assert result['error'] == 'Missing a required argument.'


def test_api_decorator_responds_to_validation_error():
    """API decorator responds appropriately to validation error."""

    @api
    def test_api_call(*args, **kwargs):
        raise ValidationError('the_field_name',
                                  'The field should be in this format.')

    result = test_api_call(json_object = True)
    assert not result['success']
    assert result['error'] == 'Validation error.'
    assert result['validation_errors'][0]['fieldname'] == 'the_field_name'
    assert result['validation_errors'][0]['message'] == 'The field should be in this format.'


def test_api_decorator_responds_to_authentication_error():
    """API decorator responds appropriately to authentication error."""

    @api
    def test_api_call(*args, **kwargs):
        return MockRequestResponse(json_data = {'status': 'Failed',
                                                'statusDescription':
                                                'Invalid authentication, incorrect auth-id or auth-password.'})

    result = test_api_call(json_object = True)
    assert not result['success']
    assert result['error'] == 'Invalid authentication, incorrect auth-id or auth-password.'


def test_api_patch_update_decorator_gets_then_updates():
    """API patch_update decorator gets before updating allowing patch updates
    with only some of the arguments."""

    @api
    def test_api_get(*args, **kwargs):
        assert len(kwargs) == 2
        assert kwargs['json_object'] == True
        assert kwargs['domain_name'] == 'my_example.com'
        return MockRequestResponse(json_data = {'key_1': 'AAA', 'key_2': 'BBB',
                                                'key_3': 'CCC', 'key_4': 'DDD'})

    @api
    @patch_update(get=test_api_get, keys=['domain_name'])
    def update(*args, **kwargs):
        return MockRequestResponse(json_data = kwargs)

    result = update(domain_name='my_example.com', key_3='ZZZ', key_4='YYY',
                    patch=True, json_object=True)

    assert result['success']
    assert result['data']['key_1'] == 'AAA'
    assert result['data']['key_2'] == 'BBB'
    assert result['data']['key_3'] == 'ZZZ'
    assert result['data']['key_4'] == 'YYY'


def test_api_patch_update_decorator_works_with_2_get_keys():
    """API patch_update decorator works with 2 get keys."""

    @api
    def test_api_get(*args, **kwargs):
        assert len(kwargs) == 3
        assert kwargs['json_object'] == True
        assert kwargs['domain_name'] == 'my_example.com'
        assert kwargs['id'] == 123
        return MockRequestResponse(json_data = {'key_1': 'AAA', 'key_2': 'BBB',
                                                'key_3': 'CCC', 'key_4': 'DDD'})

    @api
    @patch_update(get=test_api_get, keys=['domain_name', 'id'])
    def update(*args, **kwargs):
        return MockRequestResponse(json_data = kwargs)

    result = update(domain_name='my_example.com', id=123, key_3='ZZZ',
                    key_4='YYY', patch=True, json_object=True)

    assert result['success']
    assert result['data']['key_1'] == 'AAA'
    assert result['data']['key_2'] == 'BBB'
    assert result['data']['key_3'] == 'ZZZ'
    assert result['data']['key_4'] == 'YYY'


def test_api_patch_update_decorator_works_with_json_string():
    """API patch_update decorator works with json string."""

    @api
    def test_api_get(*args, **kwargs):
        assert len(kwargs) == 2
        assert kwargs['json_object'] == True
        assert kwargs['domain_name'] == 'my_example.com'
        return MockRequestResponse(json_data = {'key_1': 'AAA', 'key_2': 'BBB',
                                                'key_3': 'CCC', 'key_4': 'DDD'})

    @api
    @patch_update(get=test_api_get, keys=['domain_name'])
    def update(*args, **kwargs):
        return MockRequestResponse(json_data = kwargs)

    result = update(domain_name='my_example.com', key_3='ZZZ', key_4='YYY',
                    patch=True, json_object=False)

    assert '"key_1": "AAA"' in result
    assert '"key_2": "BBB"' in result
    assert '"key_3": "ZZZ"' in result
    assert '"key_4": "YYY"' in result
