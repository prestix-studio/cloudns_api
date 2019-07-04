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

import requests

from .api import api, patch_update
from .parameters import Parameters


@api
def get(domain_name=None):
    """Retreives the DNS SOA record for a particular domain.

    :param domain_name: string, (required) the domain name for which to
        retrieve the SOA record
    """
    url = 'https://api.cloudns.net/dns/soa-details.json'

    params = Parameters({'domain-name': domain_name})

    return requests.get(url, params=params.to_dict())


@api
@patch_update(get=get, keys=['domain_name'])
def update(domain_name=None, primary_ns=None, admin_mail=None, refresh=None,
           retry=None, expire=None, default_ttl=None, patch=False, **kwargs):
    """Updates the DNS SOA record for a particular domain.

    :param domain_name: string, (required) the domain name whose SOA record you
        want to update
    :param primary_ns: string, (required) hostname of primary nameserver
    :param admin_mail: string, (required) DNS admin's e-mail
    :param refresh: integer, (required) refresh rate from 1200 to 43200 seconds
    :param retry: integer, (required) retry rate from 180 to 2419200 seconds
    :param expire: integer, (required) expire time from 1209600 to 2419200
        seconds
    :param default_ttl: integer, (required) default TTL from 60 to 2419200
        seconds
    :param patch: boolean, whether or not to do a patch update
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

    return requests.post(url, params=params.to_dict())


def patch(*args, **kwargs):
    """A convenience function for patch updates."""
    return update(*args, patch=True, **kwargs)
