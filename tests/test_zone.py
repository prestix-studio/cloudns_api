# -*- coding: utf-8 -*-
#
# name:             test_zone.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       06/13/2019
#

"""
Functional tests for cloudns_api's zone module.
"""

from cloudns_api import zone

from .helpers import mock_get_request, mock_post_request


##
# Zone Tests

@mock_get_request()
def test_zone_list_function():
    """Zone list function sends properly formated request."""
    response = zone.list()
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/list-zones.json'
    assert payload['params']['page'] == 1
    assert payload['params']['rows-per-page'] == 10
    assert payload['params']['search'] == ''
    assert payload['params']['group-id'] == ''


@mock_get_request()
def test_zone_get_page_count_function():
    """Zone get_page_count function sends properly formated request."""
    response = zone.get_page_count(rows_per_page=10)
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/get-pages-count.json'
    assert payload['params']['rows-per-page'] == 10
    assert payload['params']['search'] == ''
    assert payload['params']['group-id'] == ''


@mock_post_request()
def test_zone_create_function():
    """Zone create function sends properly formated request."""
    response = zone.create(domain_name='example.com', zone_type='Master',
                           ns=[])
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/register.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['zone-type'] == 'Master'
    assert payload['params']['ns'] == []


@mock_post_request()
def test_soa_create_function_catches_validation_errors():
    """SOA update function catches validation errors."""
    response = zone.create('not a domain', zone_type='Master')

    assert not response.success
    assert response.json()['error'] == 'Validation error.'


@mock_get_request()
def test_zone_get_function():
    """Zone get function sends properly formated request."""
    response = zone.get(domain_name='example.com')
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/get-zone-info.json'
    assert payload['params']['domain-name'] == 'example.com'


@mock_post_request()
def test_zone_update_function():
    """Zone update function sends properly formated request."""
    response = zone.update(domain_name='example.com')
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/update-zone.json'
    assert payload['params']['domain-name'] == 'example.com'


@mock_post_request()
def test_zone_activate_function():
    """Zone actiate function sends properly formated request."""
    response = zone.activate(domain_name='example.com')
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/change-status.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['status'] == 1


@mock_post_request()
def test_zone_deactivate_function():
    """Zone deactivate function sends properly formated request."""
    response = zone.deactivate(domain_name='example.com')
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/change-status.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['status'] == 0


@mock_post_request()
def test_zone_toggle_activation_function():
    """Zone toggle_activation function sends properly formated request."""
    response = zone.toggle_activation(domain_name='example.com')
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/change-status.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert 'status' not in payload['params']


@mock_post_request()
def test_zone_delete_function():
    """Zone delete function sends properly formated request."""
    response = zone.delete(domain_name='example.com')
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/delete.json'
    assert payload['params']['domain-name'] == 'example.com'


@mock_get_request()
def test_zone_get_stats_function():
    """Zone get_stats function sends properly formated request."""
    response = zone.get_stats()
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/get-zones-stats.json'


@mock_get_request()
def test_dnssec_available():
    """Check if DNSSEC is available for the provided zone"""
    response = zone.dnssec_available('example.com')
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/is-dnssec-available.json'  # noqa: E501


@mock_post_request()
def test_dnssec_activate():
    """Activate DNSSEC for a zone."""
    response = zone.dnssec_activate('example.com')
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/activate-dnssec.json'


@mock_post_request()
def test_dnssec_deactivate():
    """Deactivate DNSSEC for a zone."""
    response = zone.dnssec_deactivate('example.com')
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/deactivate-dnssec.json'  #noqa: E501


@mock_get_request()
def test_dnssec_ds_records():
    """Get DNSSEC DS records for a zone."""
    response = zone.dnssec_ds_records('example.com')
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/get-dnssec-ds-records.json'  #noqa: E501

@mock_get_request()
def test_zone_is_updated():
    """Check if all DNS servers have been updated."""
    response = zone.is_updated('example.com')
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/is-updated.json'  #noqa: E501
