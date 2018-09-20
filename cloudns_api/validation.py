#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             validation.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       09/16/2018
#

"""
clouddns.validation
~~~~~~~~~~~~~~~~~~~

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
        super(ValidationError, self).__init__('Validation errors occured.', *args, **kwargs)

    def get_details(self):
        """Returns a list of error details."""
        return [error.details for error in self.validation_errors]


# Global value: Only use this in check_for_validation_errors and validate.
_batched_validation_errors = []


def check_for_validation_errors():
    """Checks for batched validation errors and raises a ValidationErrorsBatch
    if any are found. Otherwise, does nothing."""
    global _batched_validation_errors
    if len(_batched_validation_errors) > 0:
        raise ValidationErrorsBatch(_batched_validation_errors)


def validate(value, fieldname, *args, **kwargs):
    """Validates a value for a particular fieldtype.
    Returns a value if it is valid; raises an error otherwise.

    :param value: mixed, the value to validate
    :param fieldname: string, the fieldname to validate (determines the type of
        validation to use)
    :param optional: bool, (kwarg) if True, accept None as a valid value
    :param batch: bool, (kwarg) if True, batches errors for later processing
    """
    try:
        if kwargs.get('optional', False) and not value:
            return value
        elif not value:
            raise ValidationError(fieldname, 'This field is required.')

        if fieldname not in validation_functions:
            return value

        if validation_functions[fieldname](value, fieldname, *args, **kwargs):
            return value

        # If for some reason the validation fails, but no error was raised,
        # raise one here. This should hopefully never happen
        raise ValidationException('Unexpected validation error.')

    except ValidationError as e:
        if kwargs.get('batch', False):
            global _batched_validation_errors
            _batched_validation_errors.append(e)
        else:
            raise e


def batch_validate(value, fieldname, *args, **kwargs):
    """Helpful wrapper around validate with batch flag set to True."""
    return validate(value, fieldname, *args, batch = True, **kwargs)


def is_int(value, fieldname, min_value = None, max_value = None, **kwargs):
    """Returns the value if value is an integer (within min_value/max_value
    range); otherwise, raises a validation error."""
    try:
        value += 0  # Try it to see if it is an integer
    except TypeError:
        raise ValidationError(fieldname, 'This field must be an integer.')

    if min_value and value < min_value:
        raise ValidationError(fieldname,
                            'This field must be greater than ' + str(min_value) + '.')
    if max_value and value > max_value:
        raise ValidationError(fieldname,
                            'This field must be less than ' + str(max_value) + '.')
    return True


def is_domain_name(value, fieldname, **kwargs):
    """Returns the value if value is a valid domain name. Otherwise, raises a
    validation error."""
    if not re.match('^((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}$',
                    value):
        raise ValidationError(fieldname,
                            'This field must be a valid domain name.')
    return True


def is_email(value, fieldname, **kwargs):
    """Returns the value if value is a valid domain name. Otherwise, raises a
    validation error."""
    if not re.match('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                    value):
        raise ValidationError(fieldname,
                            'This field must be a valid email.')
    return True


def is_record_type(value, fieldname, **kwargs):
    """Returns the value if value is a valid domain recordy type. Otherwise,
    raises a validation error."""
    try:
        if value.upper() not in RECORD_TYPES:
            raise ValidationError(fieldname,
                                'This field must be a valid domain record type.')
    # If value isn't a string, upper() raises AttributeError
    except AttributeError:
        raise ValidationError(fieldname,
                              'This field must be a valid domain record type.')
    return True


RECORD_TYPES = ['A', 'AAAA', 'MX', 'CNAME', 'TXT', 'NS', 'SRV', 'WR',
                'RP', 'SSHFP', 'ALIAS', 'CAA', 'PTR' ]


def is_ttl(value, fieldname, **kwargs):
    """Returns the value if value is a valid ClouDNS ttl. Otherwise, raises a
    validation error."""
    try:
        if value.lower() not in TTL_STRINGS:
            raise ValidationError(fieldname,
                                'This field must be a valid ttl. ' + \
                                '(1 minute, 5 minutes, 15 minutes, ' + \
                                '30 minutes, 1 hour, 6 hours, 12 hours, ' + \
                                '1 day, 2 days, 3 days, 1 week, 2 weeks, ' + \
                                'or 1 month)')
    # If value isn't a string, upper() raises AttributeError
    except AttributeError:
        if value not in TTLS:
            raise ValidationError(fieldname,
                                'This field must be a valid ttl. ' + \
                                '(60, 300, 900, 1800, 3600, 21600, ' + \
                                '43200, 86400, 172800, 259200, 604800, ' + \
                                '1209600, or 2592000)')
    return True


TTL_STRINGS = ['1 minute', '5 minutes', '15 minutes', '30 minutes', '1 hour',
               '6 hours', '12 hours', '1 day', '2 days', '3 days', '1 week',
               '2 weeks', '1 month']

TTLS = [60, 300, 900, 1800, 3600, 21600, 43200, 86400, 172800, 259200, 604800,
        1209600, 2592000]


def is_redirect_type(value, fieldname, **kwargs):
    """Returns the value if it is 301 or 302. Otherwise, raises a validation
    error."""
    if value != 301 and value != 302:
        raise ValidationError(fieldname,
                            'This field must be 301 (permanent) or 302 (temporary).')
    return True


def is_caa_flag(value, fieldname, **kwargs):
    """Returns the value if it is 0 or 128. Otherwise, raises a validation
    error."""
    if value != 0 and value != 128:
        raise ValidationError(fieldname,
                            'This field must be 0 (non-critical) or 128 (critical).')
    return True


def is_caa_type(value, fieldname, **kwargs):
    """Returns the value if value is a caa type. Otherwise, raises a validation
    error."""
    try:
        if value.lower() not in CAA_TYPES:
            raise ValidationError(fieldname,
                                'This field must be one of issue, issuewild, iodef.')
    # If value isn't a string, upper() raises AttributeError
    except AttributeError:
        raise ValidationError(fieldname,
                              'This field must be one of issue, issuewild, iodef.')
    return True

CAA_TYPES = ['issue', 'issuewild', 'iodef']


def is_required(value, fieldname, **kwargs):
    """Returns the value if there is some value provided. Otherwise, raises a
    validation error."""
    if not value:
        raise ValidationError(fieldname,
                            'This field is required.')
    return True


def is_api_bool(value, fieldname, **kwargs):
    """Returns the value if value is a 0 or 1. Otherwise, raises a validation
    error."""
    if value != 0 and value != 1:
        raise ValidationError(fieldname,
                            'This field must be 0 or 1.')
    return True


def is_valid(value, fieldname, **kwargs):
    """Returns the value assuming it's valid."""
    return True


# Set up validation functions dict
validation_functions = {
    'admin-mail':       is_email,
    'bool':             is_api_bool,
    'caa_flag':         is_caa_flag,
    'caa_type':         is_caa_type,
    'caa_value':        is_valid,
    'default-ttl':      is_int,
    'domain-name':      is_domain_name,
    'email':            is_email,
    'frame':            is_api_bool,
    'frame-title':      is_valid,
    'geodns-location':  is_int,
    'integer':          is_int,
    'mail':             is_email,
    'port':             is_int,
    'primary-ns':       is_domain_name,
    'priority':         is_int,
    'record':           is_required,
    'redirect-type':    is_redirect_type,
    'refresh':          is_int,
    'required':         is_required,
    'save-path':        is_api_bool,
    'status':           is_api_bool,
    'ttl':              is_ttl,
    'txt':              is_domain_name,
    'type':             is_record_type,
    'weight':           is_int,
}
