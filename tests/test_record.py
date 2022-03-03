# -*- coding: utf-8 -*-
#
# name:             test_record.py
# author:           Harold Bradley III | Prestix Studio, LLC.
# email:            harold@prestix.studio
# created on:       05/25/2019
#

"""
Functional tests for cloudns_api's record module.
"""

from pytest import raises

from cloudns_api import record
from cloudns_api.validation import ValidationError

from .helpers import mock_get_request, mock_post_request


##
# Record Tests

@mock_get_request()
def test_record_get_available_record_types_function():
    """Record get_available_record_types function sends properly formated
    request."""
    response = record.get_available_record_types('domain')
    assert response.success

    payload = response.payload
    assert payload['url'] == \
        'https://api.cloudns.net/dns/get-available-record-types.json'
    assert payload['params']['zone-type'] == 'domain'


@mock_get_request()
def test_record_get_available_record_types_catches_validation_errors():
    """Record get_available_record_types function catches invalid record
    type."""
    response = record.get_available_record_types('not-valid')

    assert not response.success
    assert response.json()['error'] == 'Validation error.'


@mock_get_request()
def test_record_get_available_ttls_request():
    """Record get_available_ttls function sends properly formated request."""
    response = record.get_available_ttls()
    assert response.success

    payload = response.payload
    assert payload['url'] == \
        'https://api.cloudns.net/dns/get-available-ttl.json'


@mock_get_request(payload={
    'url': 'https://api.cloudns.net/dns/get-available-ttl.json',
    'params': [
        60, 300, 600, 900, 1800, 3600, 21600, 43200, 86400, 172800, 259200,
        604800, 1209600, 2592000
    ]
})
def test_record_get_available_ttls_response():
    """Record get_available_ttls function sends properly formated request."""
    response = record.get_available_ttls()
    assert response.success

    payload = response.payload
    assert payload['params'] == [
        60, 300, 600, 900, 1800, 3600, 21600, 43200, 86400, 172800, 259200,
        604800, 1209600, 2592000
    ]


@mock_get_request()
def test_record_list_function():
    """Record list function sends properly formated request."""
    response = record.list('example.com', host='ns1')
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/records.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['host'] == 'ns1'


def test_generate_record_parameters_rejects_unsupported_type():
    """The generate_record_parameters function catches unsupported
    type errors."""
    with raises(ValidationError):
        record.generate_record_parameters(record_type='ZONK')
    with raises(ValidationError):
        record.generate_record_parameters(record_type=[])


def test_generate_record_parameters_works_for_a_records():
    """The generate_record_parameters function generates A record
    parameters."""
    parameters = record.generate_record_parameters(
        domain_name='example.com', host='', record_type='A',
        record='10.10.10.10', ttl=3600)

    payload = parameters.to_dict()

    assert payload['record-type'] == 'A'
    assert payload['domain-name'] == 'example.com'
    assert payload['host'] == ''
    assert payload['record'] == '10.10.10.10'
    assert payload['ttl'] == 3600


def test_generate_record_parameters_catches_a_record_errors():
    """The generate_record_parameters function catches A record errors."""
    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', host='', record_type='A', ttl=3600,
            record='not an ip address')
    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', host='', record_type='A', ttl=3600,
            record='1000.1000.2000.3000')
    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', host='', record_type='A', ttl=3600,
            record=[])


def test_generate_record_parameters_works_for_aaaa_records():
    """The generate_record_parameters function generates AAAA record
    parameters."""
    parameters = record.generate_record_parameters(
        domain_name='example.com', host='', record_type='AAAA',
        record='2009:0db8:95a3:0000:0000:9a2e:0370:8334', ttl=3600)

    payload = parameters.to_dict()

    assert payload['record-type'] == 'AAAA'
    assert payload['domain-name'] == 'example.com'
    assert payload['host'] == ''
    assert payload['record'] == '2009:0db8:95a3:0000:0000:9a2e:0370:8334'
    assert payload['ttl'] == 3600


def test_generate_record_parameters_catches_aaaa_record_errors():
    """The generate_record_parameters function catches AAAA record errors."""
    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', host='', record_type='AAAA', ttl=3600,
            record='not an ip address')
    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', host='', record_type='AAAA', ttl=3600,
            record='fffff:aaaaa:0:0:0:0:1:0')
    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', host='', record_type='AAAA', ttl=3600,
            record=[])


def test_generate_record_parameters_works_for_mx_records():
    """The generate_record_parameters function generates MX record
    parameters."""
    parameters = record.generate_record_parameters(
        domain_name='example.com', host='mx1', record_type='MX',
        record='mail.example.com', ttl=3600)

    payload = parameters.to_dict()

    assert payload['record-type'] == 'MX'
    assert payload['domain-name'] == 'example.com'
    assert payload['host'] == 'mx1'
    assert payload['record'] == 'mail.example.com'
    assert payload['ttl'] == 3600


def test_generate_record_parameters_catches_mx_record_errors():
    """The generate_record_parameters function catches MX record errors."""
    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', host='mx1', record_type='MX', ttl=3600,
            record='not an hostname')


def test_generate_record_parameters_works_for_cname_records():
    """The generate_record_parameters function generates CNAME record
    parameters."""
    parameters = record.generate_record_parameters(
        domain_name='example.com', host='www', record_type='CNAME',
        record='example.com', ttl=3600)

    payload = parameters.to_dict()

    assert payload['record-type'] == 'CNAME'
    assert payload['domain-name'] == 'example.com'
    assert payload['host'] == 'www'
    assert payload['record'] == 'example.com'
    assert payload['ttl'] == 3600


def test_generate_record_parameters_catches_cname_record_errors():
    """The generate_record_parameters function catches CNAME record errors."""
    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', host='www', record_type='CNAME',
            ttl=3600, record='not an hostname')


def test_generate_record_parameters_works_for_txt_records():
    """The generate_record_parameters function generates TXT record
    parameters."""
    parameters = record.generate_record_parameters(
        domain_name='example.com', host='', record_type='TXT',
        record='Anything goes...', ttl=3600)

    payload = parameters.to_dict()

    assert payload['record-type'] == 'TXT'
    assert payload['domain-name'] == 'example.com'
    assert payload['host'] == ''
    assert payload['record'] == 'Anything goes...'
    assert payload['ttl'] == 3600


def test_generate_record_parameters_works_for_spf_records():
    """The generate_record_parameters function generates SPF record
    parameters."""
    parameters = record.generate_record_parameters(
        domain_name='example.com', host='', record_type='SPF',
        record='Anything goes...', ttl=3600)

    payload = parameters.to_dict()

    assert payload['record-type'] == 'SPF'
    assert payload['domain-name'] == 'example.com'
    assert payload['host'] == ''
    assert payload['record'] == 'Anything goes...'
    assert payload['ttl'] == 3600


def test_generate_record_parameters_works_for_ns_records():
    """The generate_record_parameters function generates NS record
    parameters."""
    parameters = record.generate_record_parameters(
        domain_name='example.com', host='www', record_type='NS',
        record='example.com', ttl=3600)

    payload = parameters.to_dict()

    assert payload['record-type'] == 'NS'
    assert payload['domain-name'] == 'example.com'
    assert payload['host'] == 'www'
    assert payload['record'] == 'example.com'
    assert payload['ttl'] == 3600


def test_generate_record_parameters_catches_ns_record_errors():
    """The generate_record_parameters function catches NS record errors."""
    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', host='www', record_type='NS',
            ttl=3600, record='not an hostname')


def test_generate_record_parameters_works_for_srv_records():
    """The generate_record_parameters function generates SRV record
    parameters."""
    parameters = record.generate_record_parameters(
        domain_name='example.com', host='srv1', record_type='SRV',
        record='srv.example.org', port=0, priority=10, weight=10, ttl=3600)

    payload = parameters.to_dict()

    assert payload['record-type'] == 'SRV'
    assert payload['domain-name'] == 'example.com'
    assert payload['host'] == 'srv1'
    assert payload['record'] == 'srv.example.org'
    assert payload['ttl'] == 3600


def test_generate_record_parameters_catches_srv_record_errors():
    """The generate_record_parameters function catches SRV record errors."""
    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', host='srv', record_type='SRV',
            port=0,
            priority=10, weight=10, ttl=3600, record='not an hostname')
    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', host='srv', record_type='SRV',
            port=0,
            priority=-1, weight=10, ttl=3600, record='srv.example.org')


def test_generate_record_parameters_works_for_wr_records():
    """The generate_record_parameters function generates WR record
    parameters."""
    parameters = record.generate_record_parameters(
        domain_name='example.com', host='', record_type='WR',
        redirect_type=301, record='https://example.org/path/', ttl=3600)

    payload = parameters.to_dict()

    assert payload['record-type'] == 'WR'
    assert payload['domain-name'] == 'example.com'
    assert payload['host'] == ''
    assert payload['record'] == 'https://example.org/path/'
    assert payload['ttl'] == 3600


def test_generate_record_parameters_works_for_alias_records():
    """The generate_record_parameters function generates ALIAS record
    parameters."""
    parameters = record.generate_record_parameters(
        domain_name='example.com', host='www', record_type='ALIAS',
        record='www.example.org', ttl=3600)

    payload = parameters.to_dict()

    assert payload['record-type'] == 'ALIAS'
    assert payload['domain-name'] == 'example.com'
    assert payload['host'] == 'www'
    assert payload['record'] == 'www.example.org'
    assert payload['ttl'] == 3600


def test_generate_record_parameters_catches_alias_record_errors():
    """The generate_record_parameters function catches ALIAS record errors."""
    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', host='www', record_type='ALIAS',
            ttl=3600, record='not an hostname')


def test_generate_record_parameters_works_for_rp_records():
    """The generate_record_parameters function generates RP record
    parameters."""
    parameters = record.generate_record_parameters(
        domain_name='example.com', host='', record_type='RP',
        record='an.email@example.com', ttl=3600)

    payload = parameters.to_dict()

    assert payload['record-type'] == 'RP'
    assert payload['domain-name'] == 'example.com'
    assert payload['host'] == ''
    assert payload['record'] == 'an.email@example.com'
    assert payload['ttl'] == 3600


def test_generate_record_parameters_works_for_sshfp_records():
    """The generate_record_parameters function generates SSHFP record
    parameters."""
    parameters = record.generate_record_parameters(
        domain_name='example.com', host='www', record_type='SSHFP',
        record='the fingerprint...', ttl=3600, algorithm='RSA',
        fptype='SHA-256')

    payload = parameters.to_dict()

    assert payload['record-type'] == 'SSHFP'
    assert payload['domain-name'] == 'example.com'
    assert payload['host'] == 'www'
    assert payload['record'] == 'the fingerprint...'
    assert payload['ttl'] == 3600


def test_generate_record_parameters_catches_sshfp_record_errors():
    """The generate_record_parameters function catches SSHFP record errors."""
    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', host='www', record_type='SSHFP',
            record='the fingerprint...', ttl=3600,
            algorithm='not an algorithm', fptype='SHA-356')


def test_generate_record_parameters_checks_for_invalid_type():
    """The generate_record_parameters function catches NS record errors."""
    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', record_type='bad-type')


def test_generate_record_parameters_works_for_ptr_records_v4():
    """The generate_record_parameters function generates PTR record
    parameters for IPv4."""
    parameters = record.generate_record_parameters(
        domain_name='42.2.0.192.in-addr.arpa', record_type='PTR',
        record='the.target.example.com', ttl=3600)

    payload = parameters.to_dict()

    assert payload['record-type'] == 'PTR'
    assert payload['domain-name'] == '42.2.0.192.in-addr.arpa'
    assert payload['host'] == '@'
    assert payload['record'] == 'the.target.example.com'
    assert payload['ttl'] == 3600


def test_generate_record_parameters_works_for_naptr_records():
    """The generate_record_parameters function generates NAPTR record
    parameters."""

    parameters = record.generate_record_parameters(
        domain_name='example.com', record_type='NAPTR',
        host='some.service',
        order=100, pref=10, flag=0, params='http',
        regexp='!^.*$!prodserver.example.com!',
        replace='.', ttl=3600)

    payload = parameters.to_dict()

    assert payload['record-type'] == 'NAPTR'
    assert payload['domain-name'] == 'example.com'
    assert payload['host'] == 'some.service'
    assert payload['ttl'] == 3600
    assert payload['order'] == 100
    assert payload['pref'] == 10
    assert payload['flag'] == 0
    assert payload['params'] == 'http'
    assert payload['regexp'] == '!^.*$!prodserver.example.com!'
    assert payload['replace'] == '.'


def test_generate_record_parameters_works_for_caa_records():
    """The generate_record_parameters function generates CAA record
    parameters."""

    for val in [
        {'typ': 'issue', 'val': 'ca.example.net'},
        {'typ': 'issuewild', 'val': ';'},
        {'typ': 'iodef', 'val': 'mailto:sec@example.com'},
        {'typ': 'iodef', 'val': 'https://sec.example.com'},
    ]:
        for flag in [0, 128]:
            parameters = record.generate_record_parameters(
                domain_name='example.com', record_type='CAA',
                caa_flag=flag, caa_type=val['typ'], caa_value=val['val'],
                ttl=3600)

            payload = parameters.to_dict()
            assert payload['record-type'] == 'CAA'
            assert payload['domain-name'] == 'example.com'
            assert payload['ttl'] == 3600
            assert payload['caa_flag'] == flag
            assert payload['caa_type'] == val['typ']
            assert payload['caa_value'] == val['val']


def test_generate_record_parameters_catches_caa_errors():
    """The generate_record_parameters function catches invalid CAA record
    parameters."""

    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', record_type='CAA',
            caa_flag=0, caa_type='issuwill', caa_value=';',
            ttl=3600)
    with raises(ValidationError):
        record.generate_record_parameters(
            domain_name='example.com', record_type='CAA',
            caa_flag=0, caa_type=[], caa_value=';',
            ttl=3600)


def test_generate_record_parameters_works_for_tlsa_records():
    """The generate_record_parameters function generates TLSA record
    parameters."""

    rec = '7af68c0fbebf2ed0224c1d86afcd8b122c3e9179bcb6df8cb5ad3e9960b6a8d4'
    for usage in [0, 1, 2, 3]:
        for selector in [0, 1]:
            for match in [0, 1, 2]:
                parameters = record.generate_record_parameters(
                    domain_name='example.com', record_type='TLSA',
                    tlsa_usage=usage, tlsa_selector=selector,
                    tlsa_matching_type=match,
                    record=rec,
                    host='_443._tcp',
                    ttl=3600)

                payload = parameters.to_dict()
                assert payload['record-type'] == 'TLSA'
                assert payload['domain-name'] == 'example.com'
                assert payload['host'] == '_443._tcp'
                assert payload['ttl'] == 3600
                assert payload['tlsa_usage'] == usage
                assert payload['tlsa_selector'] == selector
                assert payload['tlsa_matching_type'] == match
                assert payload['record'] == rec


def test_generate_record_parameters_includes_geo_id():
    """The generate_dns_record_parameters function includes the optional
    geo dns information"""

    parameters = record.generate_dns_record_parameters(
        domain_name='example.com', record_type='A',
        record='10.10.10.10', ttl=3600, geo_location=1)
    assert parameters['geodns-location'] == 1


@mock_post_request()
def test_record_create_function():
    """Record create function sends properly formated update request."""
    response = record.create('example.com', host='', record_type='A',
                             record='10.10.10.10', ttl=3600)

    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/add-record.json'
    assert payload['params']['record-type'] == 'A'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['host'] == ''
    assert payload['params']['record'] == '10.10.10.10'
    assert payload['params']['ttl'] == 3600


@mock_post_request()
def test_record_create_function_catches_validation_errors():
    """Record create function catches validation errors."""
    response = record.create('not a valid domain', host='', record_type='A',
                             record='10.10.10.10', ttl=3600)

    assert not response.success
    assert response.json()['error'] == 'Validation error.'


@mock_post_request()
def test_record_transfer_function():
    """Record transfer function sends properly formated get request."""
    response = record.transfer('example.com', server='1.1.1.1')
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/axfr-import.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['server'] == '1.1.1.1'


@mock_get_request()
def test_record_copy_function():
    """Record copy function sends properly formated get request."""
    response = record.copy('example.com', from_domain='example.net',
                           delete_current_records=True)
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/copy-records.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['from-domain'] == 'example.net'
    assert payload['params']['delete-current-records'] == 1


@mock_get_request(payload={
    1234: {
        'type':        'A',
        'domain-name': 'example.com',
        'record-id':   1234,
        'host':        'ns1',
        'ttl':         3600,
        'record':      '10.0.0.10',
    }
})
def test_record_get_function():
    """Record get function sends properly formated get request."""
    response = record.get('example.com', 1234)

    assert response.success

    payload = response.payload

    assert payload['type'] == 'A'
    assert payload['domain-name'] == 'example.com'
    assert payload['record-id'] == 1234
    assert payload['host'] == 'ns1'
    assert payload['ttl'] == 3600
    assert payload['record'] == '10.0.0.10'


@mock_get_request(payload={
    1234: {
        'type':        'A',
        'domain-name': 'example.com',
        'record-id':   1234,
        'host':        'ns1',
        'ttl':         3600,
        'record':      '10.0.0.10',
    }
})
def test_record_get_function_with_bad_record_id():
    """Record get function sends properly formated error message when record_id
    does not exist."""
    response = record.get('example.com', 5678)

    assert not response.success
    assert response.error == \
        'Record "5678" not found in "example.com" zone.'
    assert str(response.status_code) == '404'


@mock_get_request()
def test_record_export_function():
    """Record export function sends properly formated get request."""
    response = record.export('example.com')
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/records-export.json'
    assert payload['params']['domain-name'] == 'example.com'


@mock_get_request()
def test_record_get_dynamic_url_function():
    """Record get_dynamic_url function sends properly formated get request."""
    response = record.get_dynamic_url('example.com', record_id=1234)
    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/get-dynamic-url.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['record-id'] == 1234


@mock_post_request()
def test_record_update_function():
    """Record update function sends properly formated update request."""
    response = record.update('example.com', record_id=1234, record_type='A',
                             host='ns1', ttl=3600, record='10.0.0.10')

    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/mod-record.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['record-id'] == 1234
    assert payload['params']['host'] == 'ns1'
    assert payload['params']['ttl'] == 3600
    assert payload['params']['record'] == '10.0.0.10'


@mock_get_request(payload={
    1234: {
        'type':        'A',
        'domain-name': 'example.com',
        'record-id':   1234,
        'host':        'ns1',
        'ttl':         3600,
        'record':      '10.0.0.10',
    }
})
@mock_post_request()
def test_record_update_function_can_figure_out_record_type():
    """Record update function can figure out what record type a record
    is."""
    response = record.update('example.com', record_id=1234, host='ns1',
                             ttl=3600, record='10.0.0.10')

    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/mod-record.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['record-id'] == 1234
    assert payload['params']['host'] == 'ns1'
    assert payload['params']['ttl'] == 3600
    assert payload['params']['record'] == '10.0.0.10'


@mock_get_request(payload={
    1234: {
        'type':        'A',
        'domain-name': 'example.com',
        'record-id':   1234,
        'host':        'ns1',
        'ttl':         3600,
        'record':      '10.0.0.10',
    }
})
def test_record_update_function_with_bad_record_id():
    """Record update function sends properly formated error message
    when record_id does not exist."""
    response = record.update('example.com', record_id=5678, host='ns1',
                             ttl=3600, record='10.0.0.10')

    assert not response.success
    assert response.error == \
        'Record "5678" not found in "example.com" zone.'
    assert str(response.status_code) == '404'


@mock_get_request(payload={
    1234: {
        'type':        'A',
        'domain-name': 'example.com',
        'record-id':   1234,
        'host':        'ns1',
        'ttl':         3600,
        'record':      '10.0.0.10',
    }
})
@mock_post_request()
def test_record_update_function_using_patch():
    """Record update function sends properly formated update request
    when doing a patch update."""
    response = record.update('example.com', record_id=1234,
                             record='10.10.10.10', patch=True)

    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/mod-record.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['record-id'] == 1234
    assert payload['params']['host'] == 'ns1'
    assert payload['params']['ttl'] == 3600
    assert payload['params']['record'] == '10.10.10.10'


@mock_get_request(payload={
    1234: {
        'type':        'A',
        'domain-name': 'example.com',
        'record-id':   1234,
        'host':        'ns1',
        'ttl':         3600,
        'record':      '10.0.0.10',
    }
})
@mock_post_request()
def test_record_update_function_using_patch_helper():
    """Record update function sends properly formated update request
    when doing a patch update using the patch helper function."""
    response = record.patch('example.com', record_id=1234,
                            record='10.10.10.10')

    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/mod-record.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['record-id'] == 1234
    assert payload['params']['host'] == 'ns1'
    assert payload['params']['ttl'] == 3600
    assert payload['params']['record'] == '10.10.10.10'


@mock_get_request(payload={
    1234: {
        'type':        'A',
        'domain-name': 'example.com',
        'record-id':   1234,
        'host':        'ns1',
        'ttl':         3600,
        'record':      '10.0.0.10',
    }
})
def test_record_patch_function_with_bad_record_id():
    """Record update function sends properly formated error message
    when record_id does not exist."""
    response = record.patch('example.com', record_id=5678, host='ns1',
                            ttl=3600, record='10.0.0.10')

    assert not response.success
    assert response.error == \
        'Record "5678" not found in "example.com" zone.'
    assert str(response.status_code) == '404'


@mock_post_request()
def test_record_update_function_catches_validation_errors():
    """Record update function catches validation errors."""
    response = record.update('example.com', record_id=1234, record_type='A',
                             host='ns1', ttl='not a ttl', record='10.0.0.10')

    assert not response.success
    assert response.json()['error'] == 'Validation error.'


@mock_post_request()
def test_record_activate_function():
    """Record actiate function sends properly formated request."""
    response = record.activate(domain_name='example.com', record_id='123')
    assert response.success

    payload = response.payload
    assert payload['url'] == \
        'https://api.cloudns.net/dns/change-record-status.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['record-id'] == '123'
    assert payload['params']['status'] == 1


@mock_post_request()
def test_record_deactivate_function():
    """Record deactivate function sends properly formated request."""
    response = record.deactivate(domain_name='example.com', record_id='123')
    assert response.success

    payload = response.payload
    assert payload['url'] == \
        'https://api.cloudns.net/dns/change-record-status.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['record-id'] == '123'
    assert payload['params']['status'] == 0


@mock_post_request()
def test_record_toggle_activation_function():
    """Record toggle_activation function sends properly formated request."""
    response = record.toggle_activation(domain_name='example.com',
                                        record_id='123')
    assert response.success

    payload = response.payload
    assert payload['url'] == \
        'https://api.cloudns.net/dns/change-record-status.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['record-id'] == '123'
    assert 'status' not in payload['params']


@mock_post_request()
def test_record_delete_function():
    """Record delete function sends properly formated update request."""
    response = record.delete('example.com', record_id='123456789')

    assert response.success

    payload = response.payload
    assert payload['url'] == 'https://api.cloudns.net/dns/delete-record.json'
    assert payload['params']['domain-name'] == 'example.com'
    assert payload['params']['record-id'] == '123456789'
