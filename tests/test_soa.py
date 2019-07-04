# -*- coding: utf-8 -*-
#
# name:             test_api.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       05/26/2019
#

"""
Unit tests for cloudns_api's api soa module.
"""

from cloudns_api import soa

from .helpers import mock_get_request, mock_post_request


##
# SOA Tests

@mock_get_request()
def test_soa_get_function():
    """SOA get function sends properly formated request."""
    response = soa.get('example.com')
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/soa-details.json'
    assert payload['params']['domain-name'] == 'example.com'


@mock_post_request()
def test_soa_update_function():
    """SOA update function sends properly formated update request."""
    response = soa.update('example.com',
                          primary_ns='ns1.example.com',
                          admin_mail='test@example.com', refresh=1200,
                          retry=180, expire=1209600, default_ttl=60)

    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/modify-soa.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['primary-ns'] == 'ns1.example.com'
    assert payload['params']['admin-mail'] == 'test@example.com'
    assert payload['params']['refresh'] == 1200
    assert payload['params']['retry'] == 180
    assert payload['params']['expire'] == 1209600
    assert payload['params']['default-ttl'] == 60


@mock_get_request(payload={
    'serialNumber':  '2019051202',
    'primaryNS':     'ns1.prestix.host',
    'adminMail':     'support@prestix.host',
    'refresh':       '7200',
    'retry':         '1800',
    'expire':        '1209600',
    'defaultTTL':    '3600',
})
@mock_post_request()
def test_soa_update_function_using_patch():
    """SOA update function sends properly formated update request when doing a
    patch update."""
    response = soa.update(domain_name='example.com',
                          admin_mail='new_email@example.com', patch=True)

    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/modify-soa.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['admin-mail'] == 'new_email@example.com'


@mock_get_request(payload={
    'serialNumber':  '2019051202',
    'primaryNS':     'ns1.prestix.host',
    'adminMail':     'support@prestix.host',
    'refresh':       '7200',
    'retry':         '1800',
    'expire':        '1209600',
    'defaultTTL':    '3600',
})
@mock_post_request()
def test_soa_update_function_using_patch_helper():
    """SOA update function sends properly formated update request when doing a
    patch update using the patch helper function."""
    response = soa.patch(domain_name='example.com',
                         admin_mail='new_email@example.com')

    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/modify-soa.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['admin-mail'] == 'new_email@example.com'


@mock_post_request()
def test_soa_update_function_catches_validation_errors():
    """SOA update function catches validation errors."""
    response = soa.update('example.com',
                          primary_ns='not a domain',
                          admin_mail='test@example.com', refresh=1200,
                          retry=180, expire=1209600, default_ttl=60)

    assert not response.success
    assert response.json()['error'] == 'Validation error.'
