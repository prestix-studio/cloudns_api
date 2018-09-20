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

from __future__ import absolute_import

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


def validate(value, fieldname, *args, **kwargs):
    """Validates a value for a particular fieldtype.
    Returns a value if it is valid; raises an error otherwise.

    :param value: mixed, the value to validate
    :param fieldname: string, the fieldname to validate (determines the type of
        validation to use)
    :param optional: bool, (kwarg) if True, accept None as a valid value
    """
    if optional and not value:
        return None
    if fieldname in validation_functions:
        return validation_functions[fieldname](value, fieldname, *args, **kwargs)
    return value


def is_int(value, fieldname, min_value = None, max_value = None):
    """Returns true if value is an integer (within min_value/max_value
    range); otherwise, throws a validation error."""
    try:
        value += 0  # Try it to see if it is an integer
    except TypeError:
        raise ValidationError(fieldname, 'Value must be an integer.')

    if min_value and value < min_value:
        raise ValidationError(fieldname,
                            'Value must be greater than ' + str(min_value) + '.')
    if max_value and value > max_value:
        raise ValidationError(fieldname,
                            'Value must be less than ' + str(max_value) + '.')
    return value


def is_domain_name(value, fieldname):
    """Returns true if value is a valid domain name. Otherwise, throws a
    validation error."""
    if not re.match('^((?=[a-z0-9-]{1,63}\.)(xn--)?[a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,63}$',
                    value):
        raise ValidationError(fieldname,
                            'Value must be a valid domain name.')
    return value


def is_email(value, fieldname):
    """Returns true if value is a valid domain name. Otherwise, throws a
    validation error."""
    if not re.match('(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',
                    value):
        raise ValidationError(fieldname,
                            'Value must be a valid email.')
    return value


# Set up validation functions dict
validation_functions = {
    'domain-name':   is_domain_name,
    'admin-email':   is_email,
    'primary-ns':    is_domain_name,
    'refresh':       is_int,
}
