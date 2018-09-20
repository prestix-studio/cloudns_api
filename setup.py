#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=bad-whitespace,redefined-builtin

"""
cloudns_api setup
"""

from codecs import open
from setuptools import setup, find_packages
from os import path


with open('README.rst', 'r', 'utf-8') as f:
    README = f.read()

HERE = path.abspath(path.dirname(__file__))

setup(
    name = 'cloudns_api',
    version = '0.2',
    description = 'A python interface to the ClouDNS.net API',
    long_description = README,
    url = 'https://github.com/hbradleyiii/cloudns_api',
    download_url = 'https://github.com/hbradleyiii/cloudns_api/archive/v0.2.tar.gz',
    author = 'Harold Bradley III',
    author_email = 'harold@bradleystudio.net',
    license = 'MIT License',
    keywords = ['dns', 'dns api', 'domain name system', 'cloudns', 'server development'],
    classifiers = [  # See https://pypi.python.org/pypi?%3Aaction = list_classifiers
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    packages = find_packages(),
    install_requires = [],
    test_requires = ['pytest>=2.8.0', 'mock'],
    package_data = { '' : ['LICENSE'], },
    entry_points = { },
)
