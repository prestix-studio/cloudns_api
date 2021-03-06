#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=bad-whitespace,redefined-builtin

"""
cloudns_api setup
"""

from codecs import open
from setuptools import setup, find_packages

from cloudns_api import __version__ as version


with open('README.rst', 'r', 'utf-8') as f:
    README = f.read()

url = 'https://github.com/prestix-studio/cloudns_api/archive/v{}.tar.gz'\
        .format(version)

setup(
    name='cloudns_api',
    python_requires='>3.5',
    version=version,
    description='A python interface to the ClouDNS.net API',
    long_description=README,
    long_description_content_type='text/x-rst',
    url='https://github.com/prestix-studio/cloudns_api',
    download_url=url,
    author='Harold Bradley III | Prestix Studio, LLC',
    author_email='harold@prestix.studio',
    license='MIT License',
    keywords=['dns', 'dns api', 'domain name system', 'cloudns',
              'server development'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    install_requires=['requests'],
    test_requires=['pytest>=3', 'mock'],
    package_data={'': ['LICENSE']},
    entry_points={},
)
