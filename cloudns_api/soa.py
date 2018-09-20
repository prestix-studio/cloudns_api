#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             soa.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       09/16/2018
#

"""
clouddns.soa
~~~~~~~~~~~~

This module contains API wrapper functions for listing and updating SOA
records.
"""

from __future__ import absolute_import

from .api import api, get_auth_params, ValidationError
from .validation import batch_validate, validate
from requests import get, post


@api
def list(domain_name, **kwargs):
    """Lists the DNS SOA record for a particular domain.

    :param domain_name: string, the domain name for which to retrieve the
        SOA record
    """

    url = 'https://api.cloudns.net/dns/soa-details.json'

    params = get_auth_params()

    params['domain-name'] = validate(domain_name, 'domain-name')

    return get(url, params=params)


@api
def update(domain_name, primary_ns, admin_mail, refresh, retry, expire,
           default_ttl, **kwargs):
    """Lists the DNS SOA record for a particular domain.

    :param domain_name: string, the domain name whose SOA record you want to
        update
    :param primary_ns: string, hostname of primary nameserver
    :param admin_mail: string, DNS admin's e-mail
    :param refresh: integer, refresh rate from 1200 to 43200 seconds
    :param retry: integer, retry rate from 180 to 2419200 seconds
    :param expire: integer, expire time from 1209600 to 2419200 seconds
    :param default-ttl: integer, default TTL from 60 to 2419200 seconds
    """

    url = 'https://api.cloudns.net/dns/modify-soa.json'

    params = get_auth_params()

    params['domain-name'] = batch_validate(domain_name, 'domain-name')
    params['primary-ns'] = batch_validate(primary_ns, 'primary-ns')
    params['admin-mail'] = batch_validate(admin_mail, 'admin-mail')
    params['refresh'] = batch_validate(refresh, 'refresh', min_value = 1200,
                                       max_value = 43200)
    params['retry'] = batch_validate(retry, 'retry', min_value = 180,
                                     max_value = 2419200)
    params['expire'] = batch_validate(expire, 'expire', min_value = 1209600,
                                      max_value = 2419200)
    params['default-ttl'] = batch_validate(default_ttl, 'default-ttl',
                                           min_value = 60, max_value = 2419200)

    return post(url, params=params)
