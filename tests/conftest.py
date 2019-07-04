# -*- coding: utf-8 -*-
#
# name:             tests/conftest.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       07/04/2019
#

"""
Config hooks for tests.
"""

import cloudns_api


def pytest_configure(config):
    cloudns_api._testing = True


def pytest_unconfigure(config):
    del cloudns_api._testing
