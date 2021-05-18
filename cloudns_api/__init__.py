# -*- coding: utf-8 -*-
#
# name:             cloudns_api/__init__.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       09/15/2018
#

"""
cloudns_api
~~~~~~~~~~~

This package contains interface functions to make calls to the ClouDNS.net API.
"""

import requests  # noqa: F401

from . import api     # noqa: F401
from . import record  # noqa: F401
from . import soa     # noqa: F401
from . import zone    # noqa: F401


__title__ = 'cloudns_api'
__version__ = '0.9.5'
__author__ = 'Harold Bradley III | Prestix Studio, LLC'
__license__ = 'MIT'
__copyright__ = 'Copyright 2018-2021 Harold Bradley III | Prestix Studio, LLC'

# Soli Deo gloria. <><
