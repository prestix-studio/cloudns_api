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


def is_debug():
    env_var = environ.get('CLOUDNS_API_DEBUG')
    if env_var is None:
        return False
    return env_var.lower() in ['1', 'true', 'yes']


def get_config(env_var):
    return environ.get(env_var)
