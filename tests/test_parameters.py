# -*- coding: utf-8 -*-
#
# name:             test_parameters.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       05/26/2019
#

"""
Functional tests for cloudns_api's parameters utilities module.
"""

from os import environ
from pytest import raises

from cloudns_api.parameters import Parameters
from cloudns_api.validation import ValidationError, ValidationErrorsBatch

from .helpers import use_test_auth


##
# Parameters object Tests

@use_test_auth
def test_parameters_includes_authentication_variables(test_id, test_password):
    """Parameters object includes authentication variables by default."""
    params = Parameters({}, validate=False)

    assert params._params_with_options['auth-id'] == test_id
    assert params._params_with_options['auth-password'] == test_password


@use_test_auth
def test_parameters_authentication_variables_can_be_overriden(test_id, test_password):
    """Parameters object can override default authentication variables during
    initialization."""
    params_1 = Parameters({'auth-id': 'changed_id'}, validate=False)

    assert params_1._params_with_options['auth-id'] == 'changed_id'
    assert params_1._params_with_options['auth-password'] == test_password

    params_2 = Parameters({'auth-password': 'changed_password'}, validate=False)

    assert params_2._params_with_options['auth-id'] == test_id
    assert params_2._params_with_options['auth-password'] == 'changed_password'


@use_test_auth
def test_parameters_can_be_converted_to_dict(test_id, test_password):
    """Parameters object can be converted to a dict of parameter name and
    paramater value."""
    params = Parameters({
        'domain-name' : {
            'value' : 'example.com',
            'optional' : False,
        },
        'host' : {
            'value' : '@',
            'optional' : False,
        },
        'type' : 'TXT',
    }, validate=False)

    assert params.to_dict() == {
        'auth-id'       : test_id,
        'auth-password' : test_password,
        'domain-name'   : 'example.com',
        'host'          : '@',
        'type'          : 'TXT',
    }


def test_parameters_can_be_validated_with_validation_options():
    """Parameters object can be validated."""
    params = Parameters({
        'domain-name' : {
            'value' : '',
            'optional' : False,
        },
    }, validate=False)

    with raises(ValidationError) as exception:
        params.validate()

def test_parameters_can_be_validated_without_validation_options():
    """Parameters object can be validated without validation options."""
    params = Parameters({'domain-name' : ''}, validate=False)

    with raises(ValidationError) as exception:
        params.validate()


def test_parameters_can_catch_multiple_validation_errors():
    """Parameters object can validate multiple parameters at one time."""
    params = Parameters({
        'domain-name' : {
            'value' : '',
            'optional' : False,
        },
        'host' : {
            'value' : '',
            'optional' : False,
        },
    }, validate=False)

    with raises(ValidationErrorsBatch) as exception:
        params.validate()


def test_parameters_are_validated_on_init_by_default():
    """Parameters object can be validated on instatiation."""
    with raises(ValidationError) as exception:
        params = Parameters({
            'domain-name' : {
                'value' : '',
                'optional' : False,
            },
        })
