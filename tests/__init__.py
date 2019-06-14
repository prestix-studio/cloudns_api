# -*- coding: utf-8 -*-
#
# name:             tests/__init__.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       06/13/2019
#

"""
Test module for cloudns_api unit tests.
"""

from os import environ


environ['CLOUDNS_API_TESTING'] = 'True'
