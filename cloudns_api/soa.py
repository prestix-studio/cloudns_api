# -*- coding: utf-8 -*-
#
# name:             soa.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       09/16/2018
#

"""
cloudns_api.soa
~~~~~~~~~~~~~~~

This module contains API wrapper functions for listing and updating SOA
records.
"""

from .api import api
from .parameters import Parameters
from requests import get, post


@api
def list(domain_name=None, **kwargs):
    """Lists the DNS SOA record for a particular domain.

    :param domain_name: string, (required) the domain name for which to
        retrieve the SOA record
    """
    url = 'https://api.cloudns.net/dns/soa-details.json'

    params = Parameters({'domain-name' : domain_name})

    return get(url, params=params.to_dict())


@api
def update(domain_name=None, primary_ns=None, admin_mail=None, refresh=None,
           retry=None, expire=None, default_ttl=None, **kwargs):
    """Lists the DNS SOA record for a particular domain.

    :param domain_name: string, (required) the domain name whose SOA record you
        want to update
    :param primary_ns: string, (required) hostname of primary nameserver
    :param admin_mail: string, (required) DNS admin's e-mail
    :param refresh: integer, (required) refresh rate from 1200 to 43200 seconds
    :param retry: integer, (required) retry rate from 180 to 2419200 seconds
    :param expire: integer, (required) expire time from 1209600 to 2419200
        seconds
    :param default-ttl: integer, (required) default TTL from 60 to 2419200
        seconds
    """
    url = 'https://api.cloudns.net/dns/modify-soa.json'

    params = Parameters({
            'domain-name': domain_name,
            'primary-ns': primary_ns,
            'admin-mail': admin_mail,
            'refresh': {
                'value': refresh,
                'min_value': 1200,
                'max_value': 43200,
            },
            'retry': {
                'value': retry,
                'min_value': 180,
                'max_value': 2419200,
            },
            'expire': {
                'value': expire,
                'min_value': 1209600,
                'max_value': 2419200,
            },
            'default-ttl': {
                'value': default_ttl,
                'min_value': 60,
                'max_value': 2419200,
            },
        })

    return post(url, params=params.to_dict())
