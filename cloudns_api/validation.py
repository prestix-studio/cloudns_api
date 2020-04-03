# -*- coding: utf-8 -*-
#
# name:             validation.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       09/16/2018
#

"""
cloudns_api.validation
~~~~~~~~~~~~~~~~~~~~~~

This module contains functions to validate fields passed into the API.
"""

import re


class ValidationError(Exception):
    """Exception thrown when a validation error has occured."""
    def __init__(self, fieldname, message, *args, **kwargs):
        """Initialize ValidationError with `fieldname` and `message` values."""
        self.details = {
            'fieldname': fieldname,
            'message':   message,
        }
        super(ValidationError, self).__init__(message, *args, **kwargs)

    def get_details(self):
        """Returns a list of error details."""
        return [self.details]


class ValidationErrorsBatch(ValidationError):
    """Exception thrown when multiple validation errors have occured."""
    def __init__(self, validation_errors, *args, **kwargs):
        """Initialize ValidationError with `validation_errors` list."""
        self.validation_errors = validation_errors
        super(ValidationError, self).__init__('Validation errors occured.',
                                              *args, **kwargs)

    def get_details(self):
        """Returns a list of error details."""
        return [error.details for error in self.validation_errors]


def validate(fieldname, value, optional=False, validate_as=None, *args,
             **kwargs):
    """Validates a value for a particular fieldtype.
    Returns True if it is valid; raises an error otherwise.

    :param fieldname: string, the fieldname to validate (determines the type of
        validation to use)
    :param value: mixed, the value to validate
    :param optional: bool, if True, accept None as a valid value
    :param validate_as: string, an optional argument to specifically select a
        validation function to run. If this is not passed, the fieldname will
        be used.
    """
    if optional and not value:
        return True
    elif value is None or value == '':
        raise ValidationError(fieldname, 'This field (' + fieldname +
                              ') is required.')

    if not validate_as:
        validate_as = fieldname

    if validate_as not in validation_functions:
        return True

    if validation_functions[validate_as](value, fieldname, *args, **kwargs):
        return True

    # If for some reason the validation fails, but no error was raised,
    # raise one here. This should hopefully never happen
    raise ValidationError('Unexpected validation error.')  # pragma: no cover


##
# Specific Validation Functions

def is_algorithm(value, fieldname='algorithm', **kwargs):
    """Validates and returns True if the value is a proper algorithm.
    Otherwise, raises a validation error."""
    try:
        if value.upper() not in ALGORITHMS:
            raise ValidationError(fieldname,
                                  'This field must be RSA, DSA, ECDSA, or ' +
                                  'Ed25519.')
    # If value isn't a string, upper() raises AttributeError
    except AttributeError:
        if value not in [1, 2, 3, 4]:
            raise ValidationError(fieldname,
                                  'This field must be RSA, DSA, ECDSA, or ' +
                                  'Ed25519.')
    return True


ALGORITHMS = ['RSA', 'DSA', 'ECDSA', 'ED25519']


def is_api_bool(value, fieldname='api-bool', **kwargs):
    """Validates and returns True if the value is a 0 or 1. Otherwise, raises a
    validation error."""
    if value != 0 and value != 1:
        raise ValidationError(fieldname,
                              'This field must be 0 or 1.')
    return True


def is_caa_flag(value, fieldname='caa-flag', **kwargs):
    """Validates and returns True if the value is 0 or 128. Otherwise, raises a
    validation error."""
    if value != 0 and value != 128:
        raise ValidationError(fieldname,
                              'This field must be 0 (non-critical) or 128 ' +
                              '(critical).')
    return True


def is_caa_type(value, fieldname='caa-type', **kwargs):
    """Validates and returns True if value is a caa type. Otherwise, raises a
    validation error."""
    try:
        if value.lower() not in CAA_TYPES:
            raise ValidationError(fieldname,
                                  'This field must be one of issue, ' +
                                  'issuewild, iodef.')
    # If value isn't a string, lower() raises AttributeError
    except AttributeError:
        raise ValidationError(fieldname,
                              'This field must be one of issue, ' +
                              'issuewild, iodef.')
    return True


CAA_TYPES = ['issue', 'issuewild', 'iodef']


def is_domain_name(value, fieldname='domain-name', **kwargs):
    """Validates and returns True if the value is a valid domain name.
    Otherwise, raises a validation error."""
    if not re.match(
       r'^((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}$',
       value):
        raise ValidationError(fieldname,
                              'This field must be a valid domain name.')
    return True


def is_email(value, fieldname='email', **kwargs):
    """Validates and returns true if the value is a valid email. Otherwise,
    raises a validation error."""
    if not re.match(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                    value):
        raise ValidationError(fieldname,
                              'This field must be a valid email.')
    return True


def is_fptype(value, fieldname='fptype', **kwargs):
    """Validates and returns True if the value is a proper fingerprint type.
    Otherwise, raises a validation error."""
    try:
        if value.upper() not in FP_TYPES:
            raise ValidationError(fieldname,
                                  'This field must be one of SHA-1 or ' +
                                  'SHA-256.')
    # If value isn't a string, upper() raises AttributeError
    except AttributeError:
        if value not in [1, 2]:
            raise ValidationError(fieldname,
                                  'This field must be one of SHA-1 or ' +
                                  'SHA-256.')
    return True


FP_TYPES = ['SHA-1', 'SHA-256']


def is_int(value, fieldname='int', min_value=None, max_value=None, **kwargs):
    """Validates and returns True if the value is an integer (within
    min_value/max_value range). Otherwise, raises a validation error."""
    try:
        value += 0  # Try it to see if it is an integer
    except TypeError:
        if re.findall('[^0-9]', value):
            raise ValidationError(fieldname, 'This field must be an integer.')

    if min_value and int(value) < min_value:
        raise ValidationError(fieldname,
                              'This field must be greater than ' +
                              str(min_value) + '.')
    if max_value and int(value) > max_value:
        raise ValidationError(fieldname,
                              'This field must be less than ' +
                              str(max_value) + '.')
    return True


def is_ipv4(value, fieldname='ipv4', **kwargs):
    """Validates and returns True if the value is an IPv4 address. Otherwise,
    raises a validation error. Note that this is just a rudimentary check."""
    octets = []

    if hasattr(value, 'split'):
        octets = [o for o in value.split('.') if o.isdigit() and
                  0 <= int(o) and int(o) <= 255]

    if len(octets) != 4:
        raise ValidationError(fieldname,
                              'This field must be a valid IPv4 address.')

    return True


def is_ipv6(value, fieldname='ipv6', **kwargs):
    """Validates and returns True if the value is an IPv6 address. Otherwise,
    raises a validation error. Note that this is just a rudimentary check."""
    hextet = []

    if hasattr(value, 'split'):
        try:
            hextet = [h for h in value.split(':')
                      if 0 <= int(h, 16) and int(h, 16) <= 65535]
        except ValueError:
            hextet = []

    if len(hextet) != 8:
        raise ValidationError(fieldname,
                              'This field must be a valid IPv6 address.')

    return True


def is_record_type(value, fieldname='record-type', **kwargs):
    """Validates and returns True if the value is a valid domain record type.
    Otherwise, raises a validation error."""
    try:
        if value.upper() not in RECORD_TYPES:
            raise ValidationError(fieldname,
                                  'This field must be a valid domain record' +
                                  ' type.')
    # If value isn't a string, upper() raises AttributeError
    except AttributeError:
        raise ValidationError(fieldname,
                              'This field must be a valid domain record type.')
    return True


RECORD_TYPES = ['A', 'AAAA', 'MX', 'CNAME', 'TXT', 'SPF', 'NS', 'SRV', 'WR',
                'RP', 'SSHFP', 'ALIAS', 'CAA', 'NAPTR', 'PTR']


def is_redirect_type(value, fieldname='redirect-type', **kwargs):
    """Validates and returns True if the value is 301 or 302. Otherwise, raises
    a validation error."""
    if value != 301 and value != 302:
        raise ValidationError(fieldname,
                              'This field must be 301 (permanent) or 302 ' +
                              '(temporary).')
    return True


def is_required(value, fieldname='required', **kwargs):
    """Validates and returns True if any value is provided. Otherwise, raises a
    validation error."""
    if value is None or value == '':
        raise ValidationError(fieldname,
                              'This field is required.')
    return True


def is_rows_per_page(value, fieldname='rows-per-page', **kwargs):
    """Validates and returns True if a proper rows-per-page value is provided
    (10, 20, 30, 50, or 100). Otherwise, raises a valiadation error."""
    if value not in [10, 20, 30, 50, 100, '10', '20', '30', '50', '100']:
        raise ValidationError(fieldname,
                              'This field must be one of: 10, 20, 30, 50, or' +
                              ' 100.')
    return True


def is_tlsa_matching_type(value, fieldname='tlsa_matching_type', **kwargs):
    """Validates and returns True if a proper tlsa_matching_type value is
    provided (0, 1, 2). Otherwise, raises a valiadation error."""
    if value not in [0, 1, 2, '0', '1', '2']:
        raise ValidationError(fieldname,
                              'This field must be one of: 0, 1, or 2')
    return True


def is_tlsa_selector(value, fieldname='tlsa_selector', **kwargs):
    """Validates and returns True if a proper tlsa_selector value is provided
    (0, 1). Otherwise, raises a valiadation error."""
    if value not in [0, 1, '0', '1']:
        raise ValidationError(fieldname,
                              'This field must be one of: 0 or 1')
    return True


def is_tlsa_usage(value, fieldname='tlsa_usage', **kwargs):
    """Validates and returns True if a proper tlsa_usage value is provided (0,
    1, 2, 3). Otherwise, raises a valiadation error."""
    if value not in [0, 1, 2, 3, '0', '1', '2', '3']:
        raise ValidationError(fieldname,
                              'This field must be one of: 0, 1, 2, or 3')
    return True


def is_ttl(value, fieldname='ttl', **kwargs):
    """Validates and returns True if the value is a valid ClouDNS ttl.
    Otherwise, raises a validation error."""
    if hasattr(value, 'lower'):
        value = value.lower()

    if value not in TTLS and value not in TTL_STRINGS:
        raise ValidationError(fieldname, 'This field must be a valid ttl. ' +
                              '(1 minute, 5 minutes, 15 minutes, 30 minutes,' +
                              ' 1 hour, 6 hours, 12 hours, 1 day, 2 days, 3 ' +
                              'days, 1 week, 2 weeks, or 1 month) or (60, ' +
                              '300, 900, 1800, 3600, 21600, 43200, 86400, ' +
                              '172800, 259200, 604800, 1209600, or 2592000)')
    return True


TTL_STRINGS = ['1 minute', '5 minutes', '15 minutes', '30 minutes', '1 hour',
               '6 hours', '12 hours', '1 day', '2 days', '3 days', '1 week',
               '2 weeks', '1 month', '60', '300', '900', '1800', '3600',
               '21600', '43200', '86400', '172800', '259200', '604800',
               '1209600', '2592000']

TTLS = [60, 300, 900, 1800, 3600, 21600, 43200, 86400, 172800, 259200, 604800,
        1209600, 2592000]


def is_valid(value, fieldname='valid', **kwargs):
    """This is a stub. It always returns true."""
    return True


def is_zone_type(value, fieldname='zone-type', **kwargs):
    """Validates and returns True if the value is a valid zone type.
    Otherwise, raises a validation error."""
    if hasattr(value, 'lower'):
        value = value.lower()

    if value not in ZONE_TYPES:
        raise ValidationError(fieldname, 'This field must be a valid zone ' +
                              'type. (master, slave, parked, or geodns)')
    return True


ZONE_TYPES = ['master', 'slave', 'parked', 'geodns', 'domain', 'reverse']


# Set up validation functions dict
validation_functions = {
    'admin-mail':          is_email,
    'algorithm':           is_algorithm,
    'bool':                is_api_bool,
    'caa_flag':            is_caa_flag,
    'caa_type':            is_caa_type,
    'caa_value':           is_valid,
    'default-ttl':         is_ttl,
    'domain-name':         is_domain_name,
    'email':               is_email,
    'fptype':              is_fptype,
    'frame':               is_api_bool,
    'frame-title':         is_valid,
    'geodns-location':     is_int,
    'integer':             is_int,
    'ipv4':                is_ipv4,
    'ipv6':                is_ipv6,
    'mail':                is_email,
    'page':                is_int,
    'port':                is_int,
    'primary-ns':          is_domain_name,
    'priority':            is_int,
    'record':              is_required,
    'record-id':           is_int,
    'record-type':         is_record_type,
    'redirect-type':       is_redirect_type,
    'refresh':             is_int,
    'required':            is_required,
    'rows-per-page':       is_rows_per_page,
    'save-path':           is_api_bool,
    'status':              is_api_bool,
    'tlsa_matching_type':  is_tlsa_matching_type,
    'tlsa_selector':       is_tlsa_selector,
    'tlsa_usage':          is_tlsa_usage,
    'ttl':                 is_ttl,
    'txt':                 is_domain_name,
    'valid':               is_valid,
    'weight':              is_int,
    'zone-type':           is_zone_type,
}
