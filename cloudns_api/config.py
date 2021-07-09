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

def get_config(env_var):
    if env_var in ['CLOUDNS_API_TESTING', 'CLOUDNS_API_DEBUG']:
        return _is_true(environ.get(env_var))
    else:
        return environ.get(env_var)
