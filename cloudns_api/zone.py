# -*- coding: utf-8 -*-
#
# name:             zone.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       09/15/2018
#

"""
cloudns_api.zone
~~~~~~~~~~~~~~~~

This module contains API wrapper functions for listing, creating, updating,
getting, activating, and deleting zones.
"""

import requests

from .api import api
from .parameters import Parameters


@api
def list(page=1, rows_per_page=10, search='', group_id=''):
    """Returns a paginated list of zones

    :param page: (optional) int, current page
    :param rows_per_page: (optional) int, number of results on each page
    :param search: (optional) string used to search domain names, reverse zone
        name, or other keyword to search for in the zone names
    :param group_id: (optional) int, limits to zones within a group
    """
    url = 'https://api.cloudns.net/dns/list-zones.json'

    params = Parameters({
            'page':           page,
            'rows-per-page':  rows_per_page,
            'search': {
                'value':      search,
                'optional':   True,
            },
            'group-id': {
                'value':      group_id,
                'optional':   True,
            },
        })

    return requests.get(url, params=params.to_dict())


@api
def get_page_count(rows_per_page=10, search='', group_id=''):
    """Returns the number of pages for the full listing or search listing

    :param rows_per_page: int, number of results on each page
    :param search: (optional) string used to search domain names, reverse zone
        name, or other keyword to search for in the zone names
    :param group_id: (optional) int, limits to zones within a group
    """
    url = 'https://api.cloudns.net/dns/get-pages-count.json'

    params = Parameters({
            'rows-per-page': rows_per_page,
            'search': {
                'value':     search,
                'optional':  True,
            },
            'group-id': {
                'value':      group_id,
                'optional':   True,
            },
        })

    return requests.get(url, params=params.to_dict())


@api
def create(domain_name=None, zone_type='master', ns=[], master_ip=None):
    """Creates a new DNS zone.

    :param domain_name: string, (required) the domain name for which to
        create the zone
    :param zone_type: string, (required) mastor, slave, parked, or geodns
    :param ns: list (optional) list of nameservers used for starting ns
        record; only for master domains
    :param master_ip: string (optional, required for slave domains) master
        server IP address
    """
    url = 'https://api.cloudns.net/dns/register.json'

    param_args = {
        'domain-name': domain_name,
        'zone-type':   zone_type,
    }

    if hasattr(zone_type, 'lower') and zone_type.lower() == 'slave':
        param_args['master-ip'] = {
            'value': master_ip,
            'optional': False,
        }

    if hasattr(zone_type, 'lower') and zone_type.lower() == 'master':
        param_args['ns'] = {
            'value':    ns,
            'optional': True,
        }

    params = Parameters(param_args)

    return requests.post(url, params=params.to_dict())


@api
def get(domain_name=None):
    """Retreives the DNS zone information for a particular domain.

    :param domain_name: string, (required) the domain name for which to
        retrieve the zone information
    """
    url = 'https://api.cloudns.net/dns/get-zone-info.json'

    params = Parameters({'domain-name': domain_name})

    return requests.get(url, params=params.to_dict())


@api
def update(domain_name=None):
    """Updates the DNS zone serial number.

    :param domain_name: string, (required) the domain name for which to
        update
    """
    url = 'https://api.cloudns.net/dns/update-zone.json'

    params = Parameters({'domain-name': domain_name})

    return requests.post(url, params=params.to_dict())


@api
def activate(domain_name=None):
    """Activates the domain's zone.

    :param domain_name: string, (required) the domain name to activate
    """
    url = 'https://api.cloudns.net/dns/change-status.json'

    params = Parameters({'domain-name': domain_name, 'status': 1})

    return requests.post(url, params=params.to_dict())


@api
def deactivate(domain_name=None):
    """Deactivates the domain's zone.

    :param domain_name: string, (required) the domain name to deactivate
    """
    url = 'https://api.cloudns.net/dns/change-status.json'

    params = Parameters({'domain-name': domain_name, 'status': 0})

    return requests.post(url, params=params.to_dict())


@api
def toggle_activation(domain_name=None):
    """Toggles the domain's zone activation.

    :param domain_name: string, (required) the domain name to toggle
    """
    url = 'https://api.cloudns.net/dns/change-status.json'

    params = Parameters({'domain-name': domain_name})

    return requests.post(url, params=params.to_dict())


@api
def delete(domain_name=None):
    """Deletes a domain's zone

    :param domain_name: string, (required) the domain name for the zone to
        delete
    """
    url = 'https://api.cloudns.net/dns/delete.json'

    params = Parameters({'domain-name': domain_name})

    return requests.post(url, params=params.to_dict())


@api
def get_stats():
    """Returns the total number of zones and limits according to your ClouDNS
    plan."""
    url = 'https://api.cloudns.net/dns/get-zones-stats.json'

    params = Parameters({})

    return requests.get(url, params=params.to_dict())


@api
def dnssec_available(domain_name=None):
    """Checks if DNSSEC is available for the domain name

    :param domain_name: string, (required) the domain name to check the DNSSEC
        availability for.
    """
    url = 'https://api.cloudns.net/dns/is-dnssec-available.json'

    params = Parameters({'domain-name': domain_name})

    return requests.get(url, params=params.to_dict())


@api
def dnssec_activate(domain_name=None):
    """Activate DNSSEC for the domain's zone

    :param domain_name: string, (required) the domain name to activate DNSSEC
        for.
    """
    url = 'https://api.cloudns.net/dns/activate-dnssec.json'

    params = Parameters({'domain-name': domain_name})

    return requests.post(url, params=params.to_dict())


@api
def dnssec_deactivate(domain_name=None):
    """Deactivate DNSSEC for the domain's zone

    :param domain_name: string, (required) the domain name to deactivate DNSSEC
        for.
    """
    url = 'https://api.cloudns.net/dns/deactivate-dnssec.json'

    params = Parameters({'domain-name': domain_name})

    return requests.post(url, params=params.to_dict())


@api
def dnssec_ds_records(domain_name=None):
    """Get the DNSSEC DS records for the domain's zone

    :param domain_name: string, (required) the domain name to retrieve the
        DNSSEC DS records for.
    """
    url = 'https://api.cloudns.net/dns/get-dnssec-ds-records.json'

    params = Parameters({'domain-name': domain_name})

    return requests.get(url, params=params.to_dict())

@api
def is_updated(domain_name=None):
    """Return True if dns zone is updatd on all servers and False if it is not

    :param domain_name: string, (required) the domain name to verify.
    """
    url = 'https://api.cloudns.net/dns/is-updated.json'

    params = Parameters({'domain-name': domain_name})

    return requests.get(url, params=params.to_dict())
