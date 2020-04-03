# -*- coding: utf-8 -*-
#
# name:             config.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       05/27/2019
#

"""
cloudns_api.config
~~~~~~~~~~~~~~~~~~

This module contains the API config constants.
"""

from os import environ


def _is_true(env_var):
    if env_var is None:  # pragma: no cover
        return False
    return env_var.lower() in [1, 'true', 'yes']


CLOUDNS_API_TESTING = _is_true(environ.get('CLOUDNS_API_TESTING'))

CLOUDNS_API_AUTH_ID = environ.get('CLOUDNS_API_AUTH_ID')
CLOUDNS_API_SUB_AUTH_ID = environ.get('CLOUDNS_API_SUB_AUTH_ID')
CLOUDNS_API_SUB_AUTH_USER = environ.get('CLOUDNS_API_SUB_AUTH_USER')

CLOUDNS_API_AUTH_PASSWORD = environ.get('CLOUDNS_API_AUTH_PASSWORD')

CLOUDNS_API_DEBUG = _is_true(environ.get('CLOUDNS_API_DEBUG'))
