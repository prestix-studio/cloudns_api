# -*- coding: utf-8 -*-
#
# name:             helpers.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       05/26/2019
#

"""
Mock helpers for cloudns_api unit tests.
"""

from mock import patch

from cloudns_api.api import RequestResponseStub


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

def mock_get_request(payload=None):
    """A closure decorator to pass payload for the get_mock function.

    Note: You must use parens even when you pass no arguments.
        @mock_get_request()
    """
    def get_mock(url, params=None, payload=payload):
        """A mock get request to return the request-prepared url."""
        if not payload:
            payload = {
                'url': url,
                'params': params,
            }
        return RequestResponseStub(payload=payload)

    def decorator(test_fn):
        """Having the outer decorator allows passing arguments. This inner
        decorator is where the function is passed."""
        @patch('cloudns_api.requests.get', new=get_mock)
        def test_wrapper(*args, **kwargs):
            test_fn(*args, **kwargs)
        return test_wrapper
    return decorator


def mock_post_request(payload=None):
    """A closure decorator to pass payload for the post_mock function.

    Note: You must use parens even when you pass no arguments.
        @mock_post_request()
    """
    def post_mock(url, params=None, payload=payload):
        """A mock post request to return the request-prepared url."""
        if not payload:
            payload = {
                'url': url,
                'params': params,
            }
        return RequestResponseStub(payload=payload)

    def decorator(test_fn):
        """Having the outer decorator allows passing arguments. This inner
        decorator is where the function is passed."""
        @patch('cloudns_api.requests.post', new=post_mock)
        def test_wrapper(*args, **kwargs):
            test_fn(*args, **kwargs)
        return test_wrapper
    return decorator
