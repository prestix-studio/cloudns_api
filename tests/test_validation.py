# -*- coding: utf-8 -*-
#
# name:             test_validation.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       09/18/2018
#

"""
Functional tests for cloudns_api's validation module.
"""

from pytest import raises

from cloudns_api.validation import (
    is_algorithm,
    is_api_bool,
    is_caa_flag,
    is_caa_type,
    is_domain_name,
    is_email,
    is_fptype,
    is_int,
    is_ipv4,
    is_ipv6,
    is_record_type,
    is_redirect_type,
    is_required,
    is_rows_per_page,
    is_tlsa_matching_type,
    is_tlsa_selector,
    is_tlsa_usage,
    is_ttl,
    is_valid,
    is_zone_type,
    validate,
    ValidationError,
    ValidationErrorsBatch,
)


##
# Validation Exception Tests

def test_validation_error_exception_can_return_error_details():
    """Tests ValidationError exception."""
    validation_error = ValidationError('name-of-field', 'The error message.')

    details = validation_error.get_details()
    assert details[0]['fieldname'] == 'name-of-field'
    assert details[0]['message'] == 'The error message.'


def test_validation_errors_batch_returns_all_error_details():
    """Tests ValidationErrorsBatch exception."""
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


##
# Validate Function Tests

def test_validate_function_uses_validation_functions_dict():
    """Function validate() uses validation_functions dict to validate
    values."""
    integer = 1234
    domain = 'example.com'

    assert validate('integer', integer)
    assert validate('domain', domain)

    with raises(ValidationError):
        validate('ttl', domain)


def test_validate_function_allows_for_optional_fields():
    """Function validate() allows for optional fields."""
    assert validate('domain', None, optional=True)
    assert validate('domain', '', optional=True)

    with raises(ValidationError):
        validate('domain', '')

    with raises(ValidationError):
        validate('domain', None)

    # But this should not raise an error
    assert validate('domain', 0)


def test_validate_function_still_checks_given_optional_fields():
    """Function validate() validates optional fields if they are given."""
    optional_int = 'abcd'

    with raises(ValidationError):
        validate('ttl', optional_int)


def test_validate_function_accepts_validate_as_argument():
    """Function validate() accepts a  of additional validators to run."""
    int_value = 123
    not_int_value = 'abc'

    assert validate('new_field', int_value, validate_as='integer')

    with raises(ValidationError):
        assert validate('new_field', not_int_value, validate_as='integer')


##
# Specific Validation Functions Tests

def test_is_algorithm_validates_correctly():
    """Function is_algorithm() validates appropriately."""
    is_an_algorithm = 1
    also_is_an_algoritm = 'rsa'
    not_algorithm = 'vcr'
    also_not_algorithm = 10

    assert is_algorithm(is_an_algorithm, 'algorithm')
    assert is_algorithm(also_is_an_algoritm, 'algorithm')

    with raises(ValidationError):
        is_algorithm(not_algorithm, 'algorithm')

    with raises(ValidationError):
        is_algorithm(also_not_algorithm, 'algorithm')


def test_is_api_bool_validates_correctly():
    """Function is_api_bool() validates if any value is provided."""
    is_bool = 0
    also_bool = 1

    not_bool = 8701
    also_not_bool = 'true'

    assert is_api_bool(is_bool, 'test_bool')
    assert is_api_bool(also_bool, 'test_bool')

    with raises(ValidationError):
        is_api_bool(not_bool, 'test_bool')

    with raises(ValidationError):
        is_api_bool(also_not_bool, 'test_bool')


def test_is_caa_flag_validates_correctly():
    """Function is_caa_flag() validates true for 0 and 128."""
    is_flag = 0
    also_flag = 128
    not_flag = 1

    assert is_caa_flag(is_flag, 'caa_flag')
    assert is_caa_flag(also_flag, 'caa_flag')

    with raises(ValidationError):
        is_caa_flag(not_flag, 'caa_flag')


def test_is_caa_type_validates_correctly():
    """Function is_caa_type() validates true for 0 and 128."""
    is_type = 'issuewild'
    not_type = 'abc'

    assert is_caa_type(is_type, 'caa_type')

    with raises(ValidationError):
        is_caa_type(not_type, 'caa_type')


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
    assert exception.value.details['message'] == \
        'This field must be a valid domain name.'

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
    assert exception.value.details['message'] == \
        'This field must be a valid email.'

    with raises(ValidationError) as exception:
        is_email(also_not_an_email, 'test_email')


def test_is_fptype_validates_correctly():
    """Function is_fptype() validates appropriately."""
    is_an_fptype = 2
    also_an_fptype = 'Sha-256'
    not_an_fptype = 100
    also_not_an_fptype = 'sha-3'

    assert is_fptype(is_an_fptype, 'fptype')
    assert is_fptype(also_an_fptype, 'fptype')

    with raises(ValidationError):
        is_fptype(not_an_fptype, 'fptype')

    with raises(ValidationError):
        is_fptype(also_not_an_fptype, 'fptype')


def test_is_int_validates_integer_values():
    """Function is_int() validates if a value is an integer or not."""
    integer = 1
    also_integer = '1'
    not_integer = '1abc'
    also_not_integer = 'abc'

    assert is_int(integer, 'test_field')
    assert is_int(also_integer, 'test_field')

    with raises(ValidationError) as exception:
        is_int(not_integer, 'test_field')

    assert exception.value.details['fieldname'] == 'test_field'
    assert exception.value.details['message'] == \
        'This field must be an integer.'

    with raises(ValidationError):
        is_int(also_not_integer, 'test_field')


def test_is_int_validates_max_range():
    """Function is_int() validates if a value is less than max range."""
    just_right = 15
    too_big = 25

    assert is_int(just_right, 'test_field', min_value=10, max_value=20)

    with raises(ValidationError) as exception:
        is_int(too_big, 'test_field', min_value=10, max_value=20)

    assert exception.value.details['fieldname'] == 'test_field'
    assert exception.value.details['message'] == \
        'This field must be less than 20.'


def test_is_int_validates_min_range():
    """Function is_int() validates if a value is more than a min range."""
    just_right = 15
    too_small = 1

    assert is_int(just_right, 'test_field', min_value=10)

    with raises(ValidationError) as exception:
        is_int(too_small, 'test_field', min_value=10)

    assert exception.value.details['fieldname'] == 'test_field'
    assert exception.value.details['message'] == \
        'This field must be greater than 10.'


def test_is_ipv4_validates_ipv4_addresses():
    """Function is_ipv4() validates IPv4 addresses."""
    ip = '10.0.0.1'
    also_ip = '8.8.8.8'
    not_ip = '8.8.8.8.8'
    also_not_ip = '12345678abcdef'

    assert is_ipv4(ip)
    assert is_ipv4(also_ip)

    with raises(ValidationError):
        is_ipv4(not_ip)

    with raises(ValidationError):
        is_ipv4(also_not_ip)


def test_is_ipv6_validates_ipv6_addresses():
    """Function is_ipv6() validates IPv6 addresses."""
    ip = '2009:0db8:95a3:0000:0000:9a2e:0370:8334'
    also_ip = '2009:db8:95a3:0:0:9a2e:370:8334'
    not_ip = '8.8.8.8'
    also_not_ip = '1234:5678:abcdef'
    again_also_not_ip = '2009:0db8:95a3:0000:10000:9a2e:0370:8334'

    assert is_ipv6(ip)
    assert is_ipv6(also_ip)

    with raises(ValidationError):
        is_ipv6(not_ip)

    with raises(ValidationError):
        is_ipv6(also_not_ip)

    with raises(ValidationError):
        is_ipv6(again_also_not_ip)


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
    assert exception.value.details['message'] == \
        'This field must be a valid domain record type.'

    with raises(ValidationError) as exception:
        is_record_type(also_not_type, 'test_type')


def test_is_redirect_type_validates_correctly():
    """Function is_redirect_type() validates true for 301 and 302."""
    is_redirect = 301
    also_redirect = 302
    not_redirect = 1

    assert is_redirect_type(is_redirect, 'redirect')
    assert is_redirect_type(also_redirect, 'redirect')

    with raises(ValidationError):
        is_redirect_type(not_redirect, 'redirect')


def test_is_required_validates_correctly():
    """Function is_required() validates if any value is provided."""
    value = 'the value'
    also_value = 0
    no_value = ''
    also_no_value = None

    assert is_required(value, 'required')
    assert is_required(also_value, 'required')

    with raises(ValidationError):
        is_required(no_value, 'required')

    with raises(ValidationError):
        is_required(also_no_value, 'required')


def test_is_rows_per_page_validates_correctly():
    """Function is_rows_per_page() validates correctly."""
    valid = 10
    also_valid = '50'
    not_valid = 11
    also_not_valid = '51'

    assert is_rows_per_page(valid, 'rows-per-page')
    assert is_rows_per_page(also_valid, 'rows-per-page')

    with raises(ValidationError):
        is_rows_per_page(not_valid, 'rows-per-page')

    with raises(ValidationError):
        is_rows_per_page(also_not_valid, 'rows-per-page')


def test_is_tlsa_matching_type_validates_correctly():
    """Function is_rows_per_page() validates correctly."""
    valid = 1
    also_valid = '2'
    not_valid = 11
    also_not_valid = '51'

    assert is_tlsa_matching_type(valid, 'tlsa_matching_type')
    assert is_tlsa_matching_type(also_valid, 'tlsa_matching_type')

    with raises(ValidationError):
        is_tlsa_matching_type(not_valid, 'tlsa_matching_type')

    with raises(ValidationError):
        is_tlsa_matching_type(also_not_valid, 'tlsa_matching_type')


def test_is_tlsa_selector_validates_correctly():
    """Function is_rows_per_page() validates correctly."""
    valid = 1
    also_valid = '0'
    not_valid = 2
    also_not_valid = '3'

    assert is_tlsa_selector(valid, 'tlsa_selector')
    assert is_tlsa_selector(also_valid, 'tlsa_selector')

    with raises(ValidationError):
        is_tlsa_selector(not_valid, 'tlsa_selector')

    with raises(ValidationError):
        is_tlsa_selector(also_not_valid, 'tlsa_selector')


def test_is_tlsa_usage_validates_correctly():
    """Function is_rows_per_page() validates correctly."""
    valid = 1
    also_valid = '3'
    not_valid = 4
    also_not_valid = '51'

    assert is_tlsa_usage(valid, 'tlsa_usage')
    assert is_tlsa_usage(also_valid, 'tlsa_usage')

    with raises(ValidationError):
        is_tlsa_usage(not_valid, 'tlsa_usage')

    with raises(ValidationError):
        is_tlsa_usage(also_not_valid, 'tlsa_usage')


def test_is_ttl_validates_cloudns_ttls():
    """Function is_ttl() validates if a value is a valid ClouDNS ttl."""
    ttl = 86400
    also_ttl = '12 Hours'
    again_also_ttl = '86400'

    not_ttl = 8701
    also_not_ttl = '14 Hours'

    assert is_ttl(ttl, 'test_ttl')
    assert is_ttl(also_ttl, 'test_ttl')
    assert is_ttl(again_also_ttl, 'test_ttl')

    with raises(ValidationError):
        is_ttl(not_ttl, 'test_ttl')

    with raises(ValidationError):
        is_ttl(also_not_ttl, 'test_ttl')


def test_is_valid_always_returns_true():
    """Function is_valid() always returns true."""
    assert is_valid(None, 'test')
    assert is_valid(123, 'test')
    assert is_valid('abc', 'test')


def test_is_zone_type_validates_correctly():
    """Function is_zone_type() validates if a value is a valid ClouDNS zone
    type."""
    zone_type = 'Master'
    also_zone_type = 'slave'

    not_zone_type = 123
    also_not_zone_type = 'masterdns'

    assert is_zone_type(zone_type, 'test_zone_type')
    assert is_zone_type(also_zone_type, 'test_zone_type')

    with raises(ValidationError):
        is_zone_type(not_zone_type, 'test_zone_type')

    with raises(ValidationError):
        is_zone_type(also_not_zone_type, 'test_zone_type')
