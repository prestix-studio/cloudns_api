# -*- coding: utf-8 -*-
#
# name:             parameters.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       05/26/2019
#

"""
cloud_api.parameters
~~~~~~~~~~~~~~~~~~~~

This module contains the Parameters class for self-validating parameters
objects.

The object allows for declaring parameters with validation options for use in
self-validating (or manual validation).
"""

from .api import get_auth_params
from .validation import validate, ValidationError, ValidationErrorsBatch


class Parameters(object):
    def __init__(self, params_with_options, validate=True):
        """Initializes the Parameters object

        :param params_with_options: dict, a dict of parameters with their
            options for validating.
            Format without options:
                {
                    'fieldname' : value,
                    ...
                }
            Format with options:
                {
                    # Will be validated as 'fieldname'
                    'fieldname' : {
                        'value': value,
                        'optional': is_optional,
                        ...
                    },
                    # Will be validated as 'valid'
                    'fieldname_2' : {
                        'value': value,
                        'validate_as': 'valid',
                        ...
                    },
                    ...
                }
        :param validate: boolean, whether or not to validate parameters on
            initialization. Defaults to True.
        """
        self._params_with_options = {**get_auth_params(),
                                     **params_with_options}

        if (validate):
            self.validate()

    def to_dict(self):
        """Returns a dict of just the fieldname and values."""
        return {fieldname: options['value']
                if isinstance(options, dict) else options
                for fieldname, options in self._params_with_options.items()}

    def validate(self):
        """Validates the parameters according to the fieldname and any optional
        validation options."""
        errors = []

        for fieldname, options in self._params_with_options.items():
            if isinstance(options, dict):
                options = options.copy()
                value = options.pop('value')
            else:
                # Options variable is actually the value in this instance:
                value = options
                options = {}

            try:
                validate(fieldname, value, **options)
            except ValidationError as e:
                errors.append(e)

        if len(errors) == 1:
            raise errors[0]
        elif len(errors) > 1:
            raise ValidationErrorsBatch(errors)
