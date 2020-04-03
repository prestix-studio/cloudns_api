# -*- coding: utf-8 -*-
#
# name:             record.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       09/15/2018
#

"""
cloudns_api.record
~~~~~~~~~~~~~~~~~~

This module contains API wrapper functions for DNS listing, creating, updating,
and deleting records.

There are also a functions for activating/deactivating a record, importing
records, copying existing records

For SOA records, see soa.py
"""

import requests

from .api import (
    ApiException,
    RequestResponseStub,
    api,
    get_auth_params,
    patch_update,
)
from .parameters import Parameters
from .validation import is_record_type, ValidationError


class RecordNotFound(ApiException):
    """Record not found API exception."""
    status_code = requests.codes.NOT_FOUND


@api
def get_available_record_types(zone_type):
    """Returns available record types for a zone

    :param zone_type: string, (required) the type of the zone (domain, reverse
        or parked)
    """
    url = 'https://api.cloudns.net/dns/get-available-record-types.json'

    params = Parameters({'zone-type': zone_type})

    return requests.get(url, params=params.to_dict())


@api
def get_available_ttls():
    """Returns a list of available ttls."""
    url = 'https://api.cloudns.net/dns/get-available-ttl.json'

    return requests.get(url, params=get_auth_params())


@api
def list(domain_name=None, host=None, record_type=''):
    """Lists DNS records for a particular domain.

    :param domain_name: string, the domain name for which to retrieve the
        records
    :param host: (optional) string, a host to limit results by. Use '@' for
        domain as host.
    :param record_type: (optional) string, the record type to retrieve (ie,
        'a', 'cname', etc..., See RECORD_TYPES)
    """
    url = 'https://api.cloudns.net/dns/records.json'

    params = Parameters({
            'domain-name':  domain_name,
            'host': {
                'value':    host,
                'optional': True
            },
            'type': {
                'value':    record_type,
                'optional': True
            },
        })

    return requests.get(url, params=params.to_dict())


def generate_dns_record_parameters(domain_name=None, record_type=None, host='',
                                   record=None, ttl=None,
                                   validate_record_as='valid', **kwargs):
    """Generates parameters for a generic DNS record.

    :param domain_name: string, (required) the domain name to use for the
        record
    :param record_type: string, the type of domain to create
    :param host: string, the host for this record. Use '' (empty string) for
        top-level domain
    :param record: string, (required) the record to be added or updated
    :param ttl: int, (required) the time-to-live for this record
    :param validate_record_as: string, what to validate the record parameter
        as
    """
    params = {
        'domain-name':     domain_name,
        'host': {
            'value':       host,
            'optional':    True
        },
        'ttl':             ttl,
        'record': {
            'value':       record,
            'validate_as': validate_record_as
        }
    }

    if record_type:
        params['record-type'] = record_type

    return params


def generate_a_record_parameters(**kwargs):
    """Generates parameters for 'A' records."""
    return generate_dns_record_parameters(record_type='A',
                                          validate_record_as='ipv4',
                                          **kwargs)


def generate_aaaa_record_parameters(**kwargs):
    """Generates parameters for 'AAAA' records."""
    return generate_dns_record_parameters(record_type='AAAA',
                                          validate_record_as='ipv6',
                                          **kwargs)


def generate_mx_record_parameters(priority=10, **kwargs):
    """Generates parameters for 'MX' records.

    :param priority: int, the priority for this server record
    """
    params = generate_dns_record_parameters(record_type='MX',
                                            validate_record_as='domain-name',
                                            **kwargs)
    params['priority'] = priority

    return params


def generate_cname_record_parameters(**kwargs):
    """Generates parameters for 'CNAME' records."""
    return generate_dns_record_parameters(record_type='CNAME',
                                          validate_record_as='domain-name',
                                          **kwargs)


def generate_txt_record_parameters(**kwargs):
    """Generates parameters for 'TXT' records."""
    return generate_dns_record_parameters(record_type='TXT',
                                          validate_record_as='valid',
                                          **kwargs)


def generate_spf_record_parameters(**kwargs):
    """Generates parameters for 'SPF' records."""
    return generate_dns_record_parameters(record_type='SPF',
                                          validate_record_as='valid',
                                          **kwargs)


def generate_ns_record_parameters(**kwargs):
    """Generates parameters for 'NS' records."""
    return generate_dns_record_parameters(record_type='NS',
                                          validate_record_as='domain-name',
                                          **kwargs)


def generate_srv_record_parameters(port=None, priority=None, weight=None,
                                   **kwargs):
    """Generates parameters for 'SRV' records.

    :param port: (optional) int, port for SRV record
    :param priority:  int, priority index, prioritize the lowest indexed server
    :param weight: int, a relative weight for services with the same index
    """
    params = generate_dns_record_parameters(record_type='SRV',
                                            validate_record_as='domain-name',
                                            **kwargs)
    if port:
        params['port'] = port

    params['priority'] = priority
    params['weight'] = weight

    return params


def generate_wr_record_parameters(redirect_type=None, frame=0,
                                  frame_title='', frame_keywords='',
                                  frame_description='', **kwargs):
    """Generates parameters for 'WR' records.

    :param redirect_type:  int, 301 (permanent) or 302 (temporary) redirect
    :param frame: int [0 or 1], redirect the url in a frame so it is
        "transparent" to the user. Use '1' to enable and '0' to disable.
    :param frame_title: string, title of the frame
    :param frame_keywords: string, keywords used in the frame
    :param frame_description: string, description of the frame
    """
    params = generate_dns_record_parameters(record_type='WR',
                                            validate_record_as='valid',
                                            **kwargs)
    params['redirect-type'] = redirect_type

    params['frame'] = frame
    params['frame-title'] = {'value': frame_title, 'optional': True}
    params['frame-description'] = {'value': frame_description,
                                   'optional': True}
    params['frame-keywords'] = {'value': frame_keywords, 'optional': True}

    return params


def generate_alias_record_parameters(**kwargs):
    """Generates parameters for 'ALIAS' records."""
    return generate_dns_record_parameters(record_type='ALIAS',
                                          validate_record_as='domain-name',
                                          **kwargs)


def generate_rp_record_parameters(**kwargs):
    """Generates parameters for 'RP' records."""
    return generate_dns_record_parameters(record_type='RP',
                                          validate_record_as='valid',
                                          **kwargs)


def generate_sshfp_record_parameters(algorithm=None, fptype=None, **kwargs):
    """Generates parameters for 'SSHFP' records.

    :param algorithm: string, (required) the algorithm the record uses ('RSA',
        'DSA', 'ECDSA', or 'ED25519')
    :param fptype: int, (required) the fingerprint type of the record (SHA-1 or
        SHA-256)
    """
    params = generate_dns_record_parameters(record_type='SSHFP',
                                            validate_record_as='valid',
                                            **kwargs)
    params['algorithm'] = algorithm
    params['fptype'] = fptype

    return params


def generate_ptr_record_parameters(**kwargs):
    """Generates parameters for 'PTR' records."""
    return generate_dns_record_parameters(record_type='PTR',
                                          validate_record_as='valid',
                                          **kwargs)


def generate_naptr_record_parameters(**kwargs):
    """Generates parameters for 'NAPTR' records."""
    return generate_dns_record_parameters(record_type='NAPTR',
                                          validate_record_as='valid',
                                          **kwargs)


def generate_caa_record_parameters(caa_flag=None, caa_type='', caa_value='',
                                   **kwargs):
    """
    :param caa_flag: int, 0 - Non critical or 128 - Critical
    :param caa_type: string, type of CAA record. The available flags are issue,
        issuewild, iodef.
    :param caa_value: type is issue, caa_value can be hostname or ";". If
        caa_type is issuewild, it can be hostname or ";".  If caa_type is
        iodef, it can be "mailto:someemail@address.tld, http://example.tld or
        http://example.tld.
    """
    params = generate_dns_record_parameters(record_type='SSHFP',
                                            validate_record_as='valid',
                                            **kwargs)
    params.pop('record')

    params['caa-flag'] = caa_flag
    params['caa-type'] = caa_type
    params['caa-value'] = caa_value

    return params


def generate_tlsa_record_parameters(tlsa_usage=0, tlsa_selector=0,
                                    tlsa_matching_type=0,
                                    **kwargs):
    """
    :param tlsa_usage: int, can take one of the following values:
        0 - PKIX-TA: Certificate Authority Constraint
        1 - PKIX-EE: Service Certificate Constraint
        2 - DANE-TA: Trust Anchor Assertion
        3 - DANE-EE: Domain Issued Certificate
    :param tlsa_selector: int, can take one of the following values:
        0 - Cert: Use full certificates
        1 - SPKI: Use subject public key
    :param tlsa_matching_type: int, can take one of the following values:
        0 - Full: No Hash
        1 - SHA-256: SHA-256 Hash
        2 - SHA-512: SHA-512 hash
    """
    params = generate_dns_record_parameters(record_type='TLSA',
                                            validate_record_as='valid',
                                            **kwargs)
    params.pop('record')

    params['tlsa_usage'] = caa_flag
    params['tlsa_selector'] = caa_type
    params['tlsa_matching_type'] = caa_value

    return params


generators = {
    'A':      generate_a_record_parameters,
    'AAAA':   generate_aaaa_record_parameters,
    'MX':     generate_mx_record_parameters,
    'CNAME':  generate_cname_record_parameters,
    'TXT':    generate_txt_record_parameters,
    'SPF':    generate_spf_record_parameters,
    'NS':     generate_ns_record_parameters,
    'SRV':    generate_srv_record_parameters,
    'WR':     generate_wr_record_parameters,
    'ALIAS':  generate_alias_record_parameters,
    'RP':     generate_rp_record_parameters,
    'SSHFP':  generate_sshfp_record_parameters,
    'PTR':    generate_ptr_record_parameters,
    'NAPTR':  generate_naptr_record_parameters,
    'CAA':    generate_caa_record_parameters,
    'TLSA':   generate_tlsa_record_parameters,
}


def generate_record_parameters(record_type=None, record_id=None, **kwargs):
    """Creates and returns DNS record Parameters object for create or update
    operations.

    This function (along with the generator functions) helps to avoid code
    duplication and allows each record type to have only the specific
    parameters necessary for that type.

    :param record_type: string, (required) the record type to retrieve (ie,
        'a', 'cname', etc..., See RECORD_TYPES)
    :param record_id: int, (required for updates) the record id
    """
    if not is_record_type(record_type):
        raise ValidationError('Not a valid domain record type')

    record_parameters = generators[record_type.upper()](**kwargs)

    if record_id:
        record_parameters['record-id'] = record_id

    return Parameters(record_parameters)


@api
def create(domain_name=None, record_type=None, **kwargs):
    """Creates a DNS record.

    :param domain_name: string, (required) the domain name for which to
        retrieve the records
    :param record_type: string, (required) the type of record to create

    Other parameters are required based on the type of record you are creating.
    See the generate_{record_type}_record_parameters function.
    """
    url = 'https://api.cloudns.net/dns/add-record.json'

    params = generate_record_parameters(domain_name=domain_name,
                                        record_type=record_type, **kwargs)

    return requests.post(url, params=params.to_dict())


@api
def transfer(domain_name=None, server=None):
    """Transfers all the domain records from one DNS server to ClouDNS's
    server. The domain name must be the same on both servers.

    :param domain_name: string, the domain name to transfer
    :param server: string, the server to transfer the records from (can be a
        domain name or ip address)
    """
    url = 'https://api.cloudns.net/dns/axfr-import.json'

    params = Parameters({'domain-name': domain_name, 'server': server})

    return requests.post(url, params=params.to_dict())


@api
def copy(domain_name=None, from_domain=None, delete_current_records=False):
    """Transfers all the domain records from one DNS server to ClouDNS's
    server. The domain name must be the same on both servers.

    :param domain_name: string, the domain name to copy to
    :param from_domain: string, the domain name from which to copy
    :param delete_current_records: int, whether or not to delete the current
        records.
    """
    url = 'https://api.cloudns.net/dns/copy-records.json'

    params = Parameters({
        'domain-name': domain_name,
        'from-domain': from_domain,
        'delete-current-records': 1 if delete_current_records else 0,
    })

    return requests.get(url, params=params.to_dict())


@api
def get(domain_name=None, record_id=None):
    """Returns a specific record_id for a domain.

    This is a wrapper around the list function extracting just the specified
    record.

    :param domain_name: string, the domain name
    :param record_id: int, the ClouDNS record id to return
    """
    response = list(domain_name)

    if str(record_id) not in response.payload:
        raise RecordNotFound('Record "' + str(record_id) + '" not found in "' +
                             domain_name + '" zone.')

    return RequestResponseStub(payload=response.payload[str(record_id)],
                               status_code=response.status_code)


@api
def export(domain_name=None):
    """Exports all of the records for a domain_name in BIND format.

    :param domain_name: string, the domain name to export
    """
    url = 'https://api.cloudns.net/dns/records-export.json'

    params = Parameters({'domain-name': domain_name})

    return requests.get(url, params=params.to_dict())


@api
def get_dynamic_url(domain_name=None, record_id=None):
    """Returns a url that is used to dynamically update an A or AAAA record to
    the IP address of the device that calls the URL.

    :param domain_name: string, the domain name
    :param record_id: int, the ClouDNS record id to return. Must be an A or
        AAAA record type.
    """
    url = 'https://api.cloudns.net/dns/get-dynamic-url.json'

    params = Parameters({'domain-name': domain_name, 'record-id': record_id})

    return requests.get(url, params=params.to_dict())


@api
@patch_update(get=get, keys=['domain_name', 'record_id'])
def update(domain_name=None, record_id=None, record_type=None, patch=False,
           **kwargs):
    """Updates a DNS record.

    Record types cannot be updated, but you can pass the existing record type
    to let the api know what kind of parameters to validate against. If you do
    not pass this argument, the API will make an extra call to retrieve it for
    you.

    :param domain_name: string, (required) the domain name for which to
        retrieve the records
    :param record_id: int, (required) the record id for the record to update
    :param patch: boolean, whether or not to do a patch update
    """
    url = 'https://api.cloudns.net/dns/mod-record.json'

    if not record_type:
        response = get(domain_name, record_id)

        if not response.success:
            return RequestResponseStub(payload=response.json(),
                                       status_code=response.status_code)

        record_type = response.payload['type']

    params = generate_record_parameters(domain_name=domain_name,
                                        record_type=record_type,
                                        record_id=record_id, **kwargs)

    # Record type should not be submitted in the request to ClouDNS
    params_as_dict = params.to_dict()
    params_as_dict.pop('record-type')

    return requests.post(url, params=params_as_dict)


def patch(*args, **kwargs):
    """A convenience function for patch updates."""
    return update(*args, patch=True, **kwargs)


@api
def activate(domain_name=None, record_id=None):
    """Makes a particular record on a domain name active

    :param domain_name: string, the domain name on which to work
    :param record_id: int, record id (the id returned when listing records)
    """
    url = 'https://api.cloudns.net/dns/change-record-status.json'

    params = Parameters({'domain-name': domain_name, 'record-id': record_id,
                         'status': 1})

    return requests.post(url, params=params.to_dict())


@api
def deactivate(domain_name=None, record_id=None):
    """Makes a particular record on a domain name inactive

    :param domain_name: string, the domain name on which to work
    :param record_id: int, record id (the id returned when listing records)
    """
    url = 'https://api.cloudns.net/dns/change-record-status.json'

    params = Parameters({'domain-name': domain_name, 'record-id': record_id,
                         'status': 0})

    return requests.post(url, params=params.to_dict())


@api
def toggle_activation(domain_name=None, record_id=None):
    """Toggles active/inactive status on a particular record of a domain name.

    :param domain_name: string, the domain name on which to work
    :param record_id: int, record id (the id returned when listing records)
    """
    url = 'https://api.cloudns.net/dns/change-record-status.json'

    params = Parameters({'domain-name': domain_name, 'record-id': record_id})

    return requests.post(url, params=params.to_dict())


@api
def delete(domain_name=None, record_id=None):
    """Deletes a DNS record

    :param domain_name: string, the domain name on which to work
    :param record_id: int, the specific record id of the record to delete
    """
    url = 'https://api.cloudns.net/dns/delete-record.json'

    params = Parameters({'domain-name': domain_name, 'record-id': record_id})

    return requests.post(url, params=params.to_dict())
