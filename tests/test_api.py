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

from mock import patch
from requests import exceptions as request_exceptions

from cloudns_api.api import (
    ApiResponse,
    ApiException,
    RequestResponseStub,
    api,
    get_auth_params,
    get_login,
    get_my_ip,
    get_nameservers,
    patch_update,
    use_snake_case_keys,
)
from cloudns_api.validation import ValidationError

from .helpers import (
    mock_get_request,
    set_debug,
    set_no_debug,
    use_test_auth,
)


##
# Authentication Tests

@use_test_auth
def test_get_auth_params_returns_auth_params(test_id, test_password):
    """Function get_auth_params() returns auth params."""
    auth_params = get_auth_params()
    assert auth_params['auth-id'] == test_id
    assert auth_params['auth-password'] == test_password


@patch('cloudns_api.api.CLOUDNS_API_SUB_AUTH_ID', new=123)
@patch('cloudns_api.api.CLOUDNS_API_AUTH_ID', new=None)
def test_get_auth_params_returns_sub_auth_id():
    """Function get_auth_params() returns sub auth params."""
    auth_params = get_auth_params()
    assert auth_params['sub-auth-id'] == 123
    assert 'auth-id' not in auth_params


@patch('cloudns_api.api.CLOUDNS_API_SUB_AUTH_USER', new='sub-user')
@patch('cloudns_api.api.CLOUDNS_API_AUTH_ID', new=None)
def test_get_auth_params_returns_sub_auth_user():
    """Function get_auth_params() returns sub auth params."""
    auth_params = get_auth_params()
    assert auth_params['sub-auth-user'] == 'sub-user'
    assert 'auth-id' not in auth_params


def test_get_auth_params_returns_different_dict_every_time():
    """Function get_auth_params returns a different dict that is not modified
    from previous operations."""
    auth_params = get_auth_params()
    auth_params['a-param'] = 'a-value'
    assert 'a-param' in auth_params

    new_params = get_auth_params()
    assert 'a-param' not in new_params


##
#  SnakeCase Tests

def test_snake_case_converts_keys_to_snake_case():
    pre_normalized_dict = {
        'test':          123,
        'testTest':      123,
        'testTestTest':  123,
        'testTTL':       123,
    }

    normalized_dict = {
        'test':            123,
        'test_test':       123,
        'test_test_test':  123,
        'test_ttl':        123,
    }

    assert use_snake_case_keys(pre_normalized_dict) == normalized_dict


##
#  ApiResponse Tests

def test_api_response_can_be_initialized_with_request_response():
    """An ApiResponse object can be initialized with a request response object.
    """
    request_response = RequestResponseStub(payload={'test': 123},
                                           status_code=200)
    response = ApiResponse(request_response)

    assert not response.error
    assert response.response == request_response
    assert response.success
    assert str(response.status_code) == '200'
    assert response.payload == {'test': 123}
    assert response.json() == {
            'status_code':   200,
            'success':      True,
            'payload':      {'test': 123}
        }


def test_api_response_works_with_request_response_list():
    """An ApiResponse object works with a request response object that is a
    list."""
    request_response = RequestResponseStub(payload=[{'test1': 123},
                                                    {'test2': 456},
                                                    {'test3': 789}],
                                           status_code=200)
    response = ApiResponse(request_response)

    assert response.payload == [{'test1': 123},
                                {'test2': 456},
                                {'test3': 789}]


def test_api_response_works_with_request_response_int():
    """An ApiResponse object works with a request response object that is
    simply an integer."""
    request_response = RequestResponseStub(payload=5, status_code=200)
    response = ApiResponse(request_response)

    assert response.payload == 5


@set_no_debug
def test_api_response_can_be_initialized_without_request_response():
    """An ApiResponse object can be initialized without a request response
    object."""
    response = ApiResponse()

    assert not response.error
    assert not response.response
    assert not response.success
    assert not response.status_code
    assert response.payload == {}
    assert response.json() == {
            'status_code':  None,
            'success':      False,
            'payload':      {}
        }


@set_debug
def test_api_response_without_request_response_shows_error_when_debugging():
    """An ApiResponse object that is initialized without a request response
    object shows an error in the json when debugging."""
    response = ApiResponse()

    # It's not yet initilized with an error
    assert response.error is None

    # But it will give an error converting to json (when debug mode is set)
    assert response.json()['error'] == \
        'Response has not yet been created with a requests.response.'


def test_api_response_can_have_error_set_on_response_wout_request_response():
    """An ApiResponse object can have an error set on a response that has been
    initilized without a request response."""
    response = ApiResponse()

    response.error = 'Test error'

    assert response.error == 'Test error'
    assert response.response is None
    assert not response.success
    assert not response.status_code
    assert response.payload == {}


def test_api_response_can_be_created_with_request_response_after_init():
    """ApiResponse can be created with request response after it is
    initialized."""
    request_response = RequestResponseStub(payload={'test': 123},
                                           status_code=200)
    response = ApiResponse()
    response.create(request_response)

    assert not response.error
    assert response.response == request_response
    assert response.success
    assert str(response.status_code) == '200'
    assert response.payload == {'test': 123}
    assert response.json() == {
            'status_code':  200,
            'success':      True,
            'payload':      {'test': 123}
        }


def test_api_response_can_be_converted_to_string():
    """ApiResponse can be converted to a string."""
    request_response = RequestResponseStub(payload={'test': 123},
                                           status_code=200)
    response = ApiResponse(request_response)

    expected_string = '{"status_code": 200, "success": true, "payload": ' \
        + '{"test": 123}}'

    assert response.string() == expected_string
    assert str(response) == expected_string


def test_api_response_payload_is_normalized_to_snake_case():
    """An ApiResponse object's payload keys are normalized to snake case."""
    pre_normalized_data = {
        'test':          123,
        'testTest':      123,
        'testTestTest':  123,
        'testTTL':       123,
    }
    request_response = RequestResponseStub(payload=pre_normalized_data)
    response = ApiResponse(request_response)

    assert response.payload == {
        'test':            123,
        'test_test':       123,
        'test_test_test':  123,
        'test_ttl':        123,
    }


def test_request_response_has_status_code():
    """An RequestResponseStub object's has expected properties."""
    response = RequestResponseStub(status_code=301)

    assert str(response.status_code) == '301'

    assert str(RequestResponseStub().status_code) == '200'


def test_request_response_has_a_payload():
    """An RequestResponseStub object's has expected properties."""
    response = RequestResponseStub(payload={'abc': 123, 'def': 456})

    assert response.payload == {'abc': 123, 'def': 456}
    assert response.json() == {'abc': 123, 'def': 456}


def test_request_response_can_be_used_for_tests():
    """An RequestResponseStub object's has expected properties."""
    response = RequestResponseStub(payload={
                                   'url': 'https://example.com/',
                                   'params': {'abc': 123, 'def': 456}})

    assert response.json() == {'url': 'https://example.com/',
                               'params': {'abc': 123, 'def': 456}}


##
# API Decorator Tests

def test_api_decorator_responds_to_success():
    """API decorator responds appropriately to successful requests."""

    @api
    def test_api_call(*args, **kwargs):
        return RequestResponseStub(payload={'response': 'Testing...'})

    response = test_api_call()
    assert response.success


def test_api_decorator_responds_to_network_errors():
    """API decorator responds appropriately to network errors."""

    @api
    def test_api_call(*args, **kwargs):
        raise request_exceptions.ConnectionError()

    response = test_api_call()
    assert response.success is False
    assert response.error == 'API Network Connection error.'
    assert str(response.status_code) == '500'


def test_api_decorator_responds_to_timeout_errors():
    """API decorator responds appropriately to network timeout errors."""

    @api
    def test_api_call(*args, **kwargs):
        raise request_exceptions.ConnectTimeout()

    response = test_api_call()
    assert not response.success
    assert response.error == 'API Connection timed out.'
    assert str(response.status_code) == '504'


def test_api_decorator_responds_to_500_errors():
    """API decorator responds appropriately to non-200 status codes."""

    @api
    def test_api_call(*args, **kwargs):
        return RequestResponseStub(payload={'response': 'Testing...'},
                                   status_code='500')

    response = test_api_call()
    assert not response.success
    assert str(response.status_code) == '500'


@set_no_debug
def test_api_decorator_responds_to_bad_python_code():
    """API decorator responds appropriately to bad python code."""

    @api
    def test_api_call(*args, **kwargs):
        # Bad python code:
        return uninitialized_variable  # noqa: F821

    response = test_api_call()
    assert not response.success
    assert response.error == 'Something went wrong.'
    assert str(response.status_code) == '500'


@set_debug
def test_api_decorator_responds_specifically_to_bad_code_when_debugging():
    """API decorator responds more specifically to bad python code when in
    debug mode."""

    @api
    def test_api_call(*args, **kwargs):
        # Bad python code:
        return uninitialized_variable  # noqa: F821

    response = test_api_call()
    assert not response.success
    assert response.error == "name 'uninitialized_variable' is not defined"


@set_no_debug
def test_api_decorator_responds_to_missing_required_args():
    """API decorator responds appropriately to required missing args."""

    @api
    def test_api_call(required_arg, *args, **kwargs):
        return uninitialized_variable  # noqa: F821

    response = test_api_call()
    assert not response.success
    assert response.error == 'Something went wrong.'
    assert str(response.status_code) == '500'


def test_api_decorator_responds_to_api_exceptions():
    """API decorator responds appropriately to more generic API exceptions."""

    @api
    def test_api_call(*args, **kwargs):
        raise ApiException('There was an error.')

    response = test_api_call()
    assert not response.success
    assert response.error == 'There was an error.'
    assert str(response.status_code) == '400'


def test_api_decorator_responds_to_derived_api_exceptions():
    """API decorator responds appropriately to derived API exceptions."""

    class ChildException(ApiException):
        status_code = '403'

    @api
    def test_api_call(*args, **kwargs):
        raise ChildException('There was an error.')

    response = test_api_call()
    assert not response.success
    assert response.error == 'There was an error.'
    assert str(response.status_code) == '403'


def test_api_decorator_responds_to_validation_error():
    """API decorator responds appropriately to validation error."""

    @api
    def test_api_call(*args, **kwargs):
        raise ValidationError('the_field_name',
                              'The field should be in this format.')

    response = test_api_call()
    assert not response.success
    assert response.error == 'Validation error.'
    assert response.validation_errors[0]['fieldname'] == 'the_field_name'
    assert response.validation_errors[0]['message'] == \
        'The field should be in this format.'


def test_api_decorator_responds_to_authentication_error():
    """API decorator responds appropriately to authentication error."""

    @api
    def test_api_call(*args, **kwargs):
        return RequestResponseStub(payload={
                                   'status': 'Failed',
                                   'statusDescription':
                                   'Invalid authentication, incorrect ' +
                                   'auth-id or auth-password.'})

    response = test_api_call()
    assert not response.success
    assert response.error == \
        'Invalid authentication, incorrect auth-id or auth-password.'


def test_api_patch_update_decorator_gets_then_updates():
    """API patch_update decorator gets before updating allowing patch updates
    with only some of the arguments."""

    @api
    def test_api_get(*args, **kwargs):
        assert len(kwargs) == 1
        assert kwargs['domain_name'] == 'my_example.com'
        return RequestResponseStub(payload={'key_1': 'AAA', 'key_2': 'BBB',
                                            'key_3': 'CCC', 'key_4': 'DDD'})

    @api
    @patch_update(get=test_api_get, keys=['domain_name'])
    def update(*args, **kwargs):
        return RequestResponseStub(payload=kwargs)

    response = update(domain_name='my_example.com', key_3='ZZZ', key_4='YYY',
                      patch=True)

    assert response.success
    assert response.payload['key_1'] == 'AAA'
    assert response.payload['key_2'] == 'BBB'
    assert response.payload['key_3'] == 'ZZZ'
    assert response.payload['key_4'] == 'YYY'


def test_api_patch_update_decorator_works_with_2_get_keys():
    """API patch_update decorator works with 2 get keys."""

    @api
    def test_api_get(*args, **kwargs):
        assert len(kwargs) == 2
        assert kwargs['domain_name'] == 'my_example.com'
        assert kwargs['id'] == 123
        return RequestResponseStub(payload={'key_1': 'AAA', 'key_2': 'BBB',
                                            'key_3': 'CCC', 'key_4': 'DDD'})

    @api
    @patch_update(get=test_api_get, keys=['domain_name', 'id'])
    def update(*args, **kwargs):
        return RequestResponseStub(payload=kwargs)

    response = update(domain_name='my_example.com', id=123, key_3='ZZZ',
                      key_4='YYY', patch=True)

    assert response.success
    assert response.payload['key_1'] == 'AAA'
    assert response.payload['key_2'] == 'BBB'
    assert response.payload['key_3'] == 'ZZZ'
    assert response.payload['key_4'] == 'YYY'


def test_api_patch_update_fails_when_get_first_fails():
    """API patch_update call fails when the get request first fails."""

    @api
    def test_api_get(*args, **kwargs):
        return RequestResponseStub(payload={'status': 'Failed',
                                            'statusDescription':
                                            'Missing domain-name'})

    @api
    @patch_update(get=test_api_get, keys=['domain_name'])
    def update(*args, **kwargs):
        return RequestResponseStub(payload=kwargs)

    response = update(domain_name='my_example.com', key_3='ZZZ', key_4='YYY',
                      patch=True)

    assert not response.success
    assert response.error == 'Missing domain-name'


@use_test_auth
@mock_get_request()
def test_simple_api_functions(test_id, test_password):
    """Tests that get_login, get_nameservers, and get_my_ip send properly
    formated requests."""
    expected_payload = {
        'auth-id': test_id,
        'auth-password': test_password,
    }

    response = get_login()
    assert response.payload['params'] == expected_payload

    response = get_nameservers()
    assert response.payload['params'] == expected_payload

    response = get_my_ip()
    assert response.payload['params'] == expected_payload
