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


CLOUDNS_API_AUTH_ID = environ.get('CLOUDNS_API_AUTH_ID')
if not CLOUDNS_API_AUTH_ID:
    raise EnvironmentError(
        'Environment variable "CLOUDNS_API_AUTH_ID" not set.'
    )

CLOUDNS_API_AUTH_PASSWORD = environ.get('CLOUDNS_API_AUTH_PASSWORD')
if not CLOUDNS_API_AUTH_PASSWORD:
    raise EnvironmentError(
        'Environment variable "CLOUDNS_API_AUTH_PASSWORD" not set.'
    )

CLOUDNS_API_DEBUG = environ.get('CLOUDNS_DEBUG') or False
