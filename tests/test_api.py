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

# Set environment vars to test vars
environ['CLOUDNS_AUTH_ID'] = 'user_id_123'
environ['CLOUDNS_AUTH_PASSWORD'] = 'user_password_123'
orig_clouds_auth_id = environ.get('CLOUDNS_AUTH_ID')
orig_clouds_auth_password = environ.get('CLOUDNS_AUTH_PASSWORD')

# Import only after changing environment variables to test vars
from cloudns_api import api

# Reset environment variables to original state
environ['CLOUDNS_AUTH_ID'] = orig_clouds_auth_id
environ['CLOUDNS_AUTH_PASSWORD'] = orig_clouds_auth_password


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
