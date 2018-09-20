#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             test_validation.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       09/18/2018
#

"""
Functional tests for cloudns-api's validation module.
"""


from cloudns_api.validation import batch_validate, check_for_validation_errors
from cloudns_api.validation import is_domain_name, is_int, is_email
from cloudns_api.validation import is_record_type, is_required, validate
from cloudns_api.validation import ValidationError, ValidationErrorsBatch
from pytest import raises


def test_validation_error_exception_can_return_error_details():
    validation_error = ValidationError('name-of-field', 'The error message.')

    details = validation_error.get_details()
    assert details[0]['fieldname'] == 'name-of-field'
    assert details[0]['message'] == 'The error message.'


def test_validation_errors_batch_returns_all_error_details():
    error_1 = ValidationError('first-field', 'The first error message.')
    error_2 = ValidationError('second-field', 'The second error message.')
    error_3 = ValidationError('third-field', 'The third error message.')

    errors = [error_1, error_2, error_3]

    validation_errors_batch = ValidationErrorsBatch(errors)
    details = validation_errors_batch.get_details()

    assert details[0]['fieldname'] == 'first-field'
    assert details[0]['message'] == 'The first error message.'
    assert details[1]['fieldname'] == 'second-field'
    assert details[1]['message'] == 'The second error message.'
    assert details[2]['fieldname'] == 'third-field'
    assert details[2]['message'] == 'The third error message.'


def test_is_int_validates_integer_values():
    """Function is_int() validates if a value is an integer or not."""
    integer = 1
    not_integer = '1'
    also_not_integer = 'abc'

    assert is_int(integer, 'test_field')

    with raises(ValidationError) as exception:
        is_int(not_integer, 'test_field')

    assert exception.value.details['fieldname'] == 'test_field'
    assert exception.value.details['message'] == 'This field must be an integer.'

    with raises(ValidationError):
        is_int(also_not_integer, 'test_field')


def test_is_int_validates_max_range():
    """Function is_int() validates if a value is less than max range."""
    too_small = 1
    just_right = 15
    too_big = 25

    assert is_int(just_right, 'test_field', max_value = 20)

    with raises(ValidationError) as exception:
        is_int(too_big, 'test_field', max_value = 20)

    assert exception.value.details['fieldname'] == 'test_field'
    assert exception.value.details['message'] == 'This field must be less than 20.'


def test_is_int_validates_min_range():
    """Function is_int() validates if a value is more than a min range."""
    just_right = 15
    too_small = 1

    assert is_int(just_right, 'test_field', min_value = 10)

    with raises(ValidationError) as exception:
        is_int(too_small, 'test_field', min_value = 10)

    assert exception.value.details['fieldname'] == 'test_field'
    assert exception.value.details['message'] == 'This field must be greater than 10.'


def test_is_domain_name_validates_domain_names():
    """Function is_domain_name() validates if a value is a valid domain
    name."""
    domain_name = 'example.com'
    also_a_domain_name = 'sub.example.com'

    not_a_domain_name = 'example@gmail.com'
    also_not_a_domain_name = 'http://example.com/'

    assert is_domain_name(domain_name, 'test_domain_field')
    assert is_domain_name(also_a_domain_name, 'test_domain_field')

    with raises(ValidationError) as exception:
        is_domain_name(not_a_domain_name, 'test_domain_field')

    assert exception.value.details['fieldname'] == 'test_domain_field'
    assert exception.value.details['message'] == 'This field must be a valid domain name.'

    with raises(ValidationError) as exception:
        is_domain_name(also_not_a_domain_name, 'test_domain_field')


def test_is_email_validates_emails():
    """Function is_email() validates if a value is a valid email."""
    email = 'test@example.com'
    also_an_email = 'test+spam@example.com'

    not_an_email = 'example@@com'
    also_not_an_email = 'http://example.com/'

    assert is_email(email, 'test_email')
    assert is_email(also_an_email, 'test_email')

    with raises(ValidationError) as exception:
        is_email(not_an_email, 'test_email')

    assert exception.value.details['fieldname'] == 'test_email'
    assert exception.value.details['message'] == 'This field must be a valid email.'

    with raises(ValidationError) as exception:
        is_email(also_not_an_email, 'test_email')


def test_is_record_type_validates_types():
    """Function is_record_type() validates if a value is a valid domain record
    type."""
    is_type = 'Mx'
    also_type = 'aaaa'

    not_type = 'XM'
    also_not_type = 123

    assert is_record_type(is_type, 'test_type')
    assert is_record_type(also_type, 'test_type')

    with raises(ValidationError) as exception:
        is_record_type(not_type, 'test_type')

    assert exception.value.details['fieldname'] == 'test_type'
    assert exception.value.details['message'] == 'This field must be a valid domain record type.'

    with raises(ValidationError) as exception:
        is_record_type(also_not_type, 'test_type')


def test_is_required_validates_correctly():
    """Function is_required() validates if any value is provided."""
    value = 'the value'

    assert is_required(value, 'required')


def test_validate_function_uses_validation_functions_dict():
    """Function validate() uses validation_functions dict to validate
    values."""
    integer = 1234
    domain = 'example.com'

    assert validate(integer, 'integer')
    assert validate(domain, 'domain')

    with raises(ValidationError) as exception:
        validate(domain, 'ttl')


def test_validate_function_allows_for_optional_fields():
    """Function validate() allows for optional fields."""
    optional = None

    # validate domain none, empty string, is optional a kwarg?
    assert None == validate(optional, 'domain', optional = True)

    with raises(ValidationError) as exception:
        validate(optional, 'domain')


def test_validate_function_still_checks_given_optional_fields():
    """Function is_email() validates if a value is a valid email."""
    optional_int = 'abcd'

    with raises(ValidationError) as exception:
        validate(optional_int, 'ttl')


def test_batch_validate_batches_validation_errors():
    """Function batch_validate() batches (holds) validation errors until
    check_for_validation_errors() is called."""

    not_an_email = 'example@@com'
    not_an_int = 'abcd'
    not_a_domain = '/domain/'

    batch_validate(not_an_email, 'email')
    batch_validate(not_an_int, 'int')
    batch_validate(not_a_domain, 'domain-name')

    with raises(ValidationError) as exception:
        check_for_validation_errors()

    # It can be caught by both exception handlers
    with raises(ValidationErrorsBatch) as exception:
        check_for_validation_errors()
