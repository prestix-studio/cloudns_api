# -*- coding: utf-8 -*-
#
# name:             helpers.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       05/26/2019
#

"""
Mock and fixture helpers for cloudns_api unit tests.
"""

from mock import patch
from pytest import fixture

from cloudns_api.config import (
    CLOUDNS_API_AUTH_ID,
    CLOUDNS_API_AUTH_PASSWORD,
    CLOUDNS_API_DEBUG,
)


##
# Config patches

TEST_ID = 'test-auth-id'
TEST_PASSWORD = 'test-auth-password'

def use_test_auth(test_fn):
    @patch('cloudns_api.api.CLOUDNS_API_AUTH_ID', new=TEST_ID)
    @patch('cloudns_api.api.CLOUDNS_API_AUTH_PASSWORD', new=TEST_PASSWORD)
    def test_wrapper(*args, **kwargs):
        test_fn(*args, test_id=TEST_ID, test_password=TEST_PASSWORD, **kwargs)
    return test_wrapper


def set_debug(test_fn):
    @patch('cloudns_api.api.CLOUDNS_API_DEBUG', new=True)
    def test_wrapper(*args, **kwargs):
        test_fn(*args, **kwargs)
    return test_wrapper


def set_no_debug(test_fn):
    @patch('cloudns_api.api.CLOUDNS_API_DEBUG', new=False)
    def test_wrapper(*args, **kwargs):
        test_fn(*args, **kwargs)
    return test_wrapper


##
# Request Mock functions

class MockRequestResponse:
    def __init__(self, url='', params=None, json_data=None, status_code=200):
        """Mocks the requests response object for testing.

        :param url: string, the url that was called in the get or post request.
        :param params: dict, parameters to be passed to requests.
        :param json_data: dict, json data to be returned in the json() method.
        :param status_code: integer, the status code to return in the test.
            Defaults to 200.
        """
        self.url = url
        self.json_data = json_data
        self.params = params
        self.status_code = status_code

    def json(self):
        """Mocks the json object method. If the response was initialized with
        json_data, it will return that. Otherwise, it will return simply the
        url and params that it was defined with."""
        if self.json_data:
            return self.json_data
        else:
            return {
                'url' : self.url,
                'params' : self.params,
            }


def mock_get_request(json_data=None):
    """A closure decorator to pass json_data for the get_mock function.

    Note: You must use parens even when you pass no arguments.
        @mock_get_request()
    """
    def get_mock(url, params=None):
        """A mock get request to return the request-prepared url."""
        return MockRequestResponse(url, params=params, json_data=json_data)

    def decorator(test_fn):
        """Having the outer decorator allows passing arguments. This inner
        decorator is where the function is passed."""
        @patch('cloudns_api.soa.requests.get', new=get_mock)
        def test_wrapper(*args, **kwargs):
            test_fn(*args, **kwargs)
        return test_wrapper
    return decorator


def mock_post_request(json_data=None):
    """A closure decorator to pass json_data for the post_mock function.

    Note: You must use parens even when you pass no arguments.
        @mock_post_request()
    """
    def post_mock(url, params=None, json_data=None):
        """A mock post request to return the request-prepared url."""
        return MockRequestResponse(url, params=params, json_data=json_data)

    def decorator(test_fn):
        """Having the outer decorator allows passing arguments. This inner
        decorator is where the function is passed."""
        @patch('cloudns_api.soa.requests.post', new=post_mock)
        def test_wrapper(*args, **kwargs):
            test_fn(*args, **kwargs)
        return test_wrapper
    return decorator
