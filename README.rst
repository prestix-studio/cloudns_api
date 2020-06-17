cloudns_api
###########

A Python 3 interface to the ClouDNS.net API
===========================================

Please note that this is still in Beta. Use at your own risk.

This project is an independent project not developed by
`CloudNS.net <https://cloudns.net>`__.

The interface is designed to be simple and intuitive. Entities are represented
as modules. Each has a list, create, update, and delete function (when
appropriate, ie, you cannot delete an SOA record). Some entities have functions
specific to them, but whenever possible, the arguments are consistent. One of
the major goals of this project is code readability.

Another major goal is for the code to have 90%+ test coverage.

For documentation on the `CloudNS.net <https://cloudns.net>`__ API see `here
<https://www.cloudns.net/wiki/article/41/>`__.

Please submit any bug reports and bug fixes on github `here
<https://github.com/prestix-studio/>`__.



Installing and including in projects
====================================


Installing cloudns_api
----------------------

.. code:: bash

    $ pip install cloudns_api


In order to authenticate, you must first generate a CloudNS auth user or sub
user and password combination. (See `here
<https://www.cloudns.net/wiki/article/42/>`__ for instructions.) Then you must
set the appropriate username and password values as environment variables as
follows:

.. code:: bash

    # USERNAME:
    export CLOUDNS_API_AUTH_ID=my_user
    #      - or -
    export CLOUDNS_API_SUB_AUTH_ID=my_user
    #      - or -
    export CLOUDNS_API_SUB_AUTH_USER=my_user

    # PASSWORD:
    # This should be the password that corresponds to the above user or sub
    # user.
    export CLOUDNS_API_AUTH_PASSWORD=my_password


When you are debugging, you can set the environment variable
`CLOUDNS_API_DEBUG` to True:

.. code:: bash

    export CLOUDNS_API_DEBUG=True


To make things easier, you could put these in your python virtual environment
or use a package like
`python-dotenv <https://github.com/theskumar/python-dotenv>`__ to automatically
load your environment variables. Be sure to *not* include your private username
and password in your public repositories.


Running Tests
-------------

.. code:: bash

    $ cd <cloudns_api directory>
    $ py.test

    $ py.test -x                    # Stop on failures
    $ py.test tests/test_record.py  # Specific test
    $ py.test -k validate           # Run tests with 'validate' in the name


Importing and Basic Usage
-------------------------

.. code:: python

    >>> import cloudns_api

    >>> response = cloudns_api.zone.list(search='example')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      [
                {
                    "name":     "example.com",
                    "type":     "master",
                    "zone":     "domain",
                    "status":   "1"
                },
                {
                    "name":     "example.net",
                    "type":     "master",
                    "zone":     "domain",
                    "status":   "1"
                },
                {
                    "name":     "example.org",
                    "type":     "master",
                    "zone":     "domain",
                    "status":   "1"
                }
            ]
        }



API Reference
=============

Introduction
------------

We have created the API to be consistent and predictable. API calls usually
include `list`, `create`, `get`, and `update` functions that do exactly what
they say. Arguments are passed in a consistent manner across all functions.
When an argument accepts an integer, it can be passed as an integer or a string
of that integer.

All arguments are passed to the API functions as keyword arguments. Each API
function turns these arguments into a `Parameters` instance. The construction
of the `Parameters` instance can also include information for validating the
arguments. This validation happens by default when the object is instantiated.
If a validation error occurs, the exception is thrown and handled in the api
decorator. A parameter is required unless the optional flag is set to `True`.
The name of the parameter is matched to a validation function unless the
`validate_as` option is set on that particular parameter. The `Parameters`
object has a to_dict() method that returns the parameters as a key-value dict
to be passed on to the CloudNS API using requests.

The CloudNS API sometimes uses camel case and sometimes uses dashes in its
parameters. In our API, we convert both of these to snake case for consistency
and in order to be "pythonic".

API `update` functions require all required parameters to be passed. This can
be inconvenient at times, so cloudns_api includes an argument `patch` that when
set to `True` allows you to pass only arguments you wish to change. Behind the
scenes, the API will get the existing data and merge it with the new data for
the update call. We've also included the convenient `patch` function as a
wrapper around `update` with the `patch` argument set to `True`.

The cloudns_api includes these two helpful functions for checking your login
credentials and retrieving your CloudNS nameservers:

.. code:: python

    >>> print(cloudns_api.api.get_login())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "status":             "Success",
                "status_description": "Success login."
            }
        }

    >>> print(cloudns_api.api.get_nameservers())


ApiResponse
^^^^^^^^^^^

All API calls return an `ApiResponse` instance. The `ApiResponse` object is a
wrapper around the basic response object from the `requests
<https://github.com/kennethreitz/requests>`__ library. We've added a few
properties and functions specific to our needs here.

.. code:: python

    >>> print(response.success)      # See if a response succeeded

    >>> print(response.status_code)  # Get the status of a response

    >>> print(response.payload)      # The payload of the response
                                     # Note that the parameters are converted
                                     # to camel case here.

    >>> print(response.json())       # Get the response as json object

    >>> print(response.string())     # Get the response as json string


ApiParameter
^^^^^^^^^^^^

The `ApiParameter` object is responsible for describing the kinds of parameters
to pass to the api function and how these parameters should be validated.
Understanding the ApiParameter object is not necessary for using the API, but
can be helpful to see what is going on under the hood.

By default, an ApiParameter validates its parameters upon initialization. But
if the `validate` parameter is set to false, this can be deferred until later.
You can then call the `validate()` method to manually validate the parameters.

.. code:: python

    >>> print(parameters.validate())  # Validates the parameters according to
                                      # their definitions

    >>> print(response.to_dict())  # Returns the parameters as a dict. Used
                                   # when passing the parameters to requests.

A full discription of how an ApiParameter object and its parameter definition
works can be found in the `cloudns_api/parameters.py` file. You may also need
to reference the `cloudns_api/validation.py` module to see how validation
works.


DNS ZONE
--------

Parameters:

+ page - int/string (optional) Page number to show.
+ rows_per_page - int/string (optional) Number of rows per page to show.
+ search - string (optional) Optional string to filter results by.
+ group_id - int/string (optional) Optional group id to filter results by.

Response Parameters:

+ name - Domain name.
+ type - Zone type (Master, Slave, Parked, GeoDNS)
+ zone -
+ status - active (1) or inactive(0)


Listing DNS Zones
^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.zone.list(search='example')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      [
                {
                    "name":     "example.com",
                    "type":     "master",
                    "zone":     "domain",
                    "status":   "1"
                },
                {
                    "name":     "example.net",
                    "type":     "master",
                    "zone":     "domain",
                    "status":   "1"
                },
                {
                    "name":     "example.org",
                    "type":     "master",
                    "zone":     "domain",
                    "status":   "1"
                }
            ]
        }

    >>> print(cloudns_api.zone.get_page_count(rows_per_page=10))  # Get page count


Creating DNS Zones
^^^^^^^^^^^^^^^^^^

NOTE: The nameserver argument doesn't seem to currently work on ClouDNS's
servers.

.. code:: python

    >>> response = cloudns_api.zone.create(domain_name='example.com',
                                           zone_type='master')
    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "status": "Success",
                "status_description":
                    "Domain zone example.com was created successfully."
            }
        }


Getting a DNS Zone
^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.zone.get(domain_name='example.com')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "name":     "example.com",
                "type":     "master",
                "zone":     "domain",
                "status":   "1"
            }
        }


Updating a DNS Zone Serial Number
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.zone.update(domain_name='example.com')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "status": "Success",
                "status_description":
                    "Domain zone example.com was updated successfully."
            }
        }


Activating/Deactivating a DNS Zone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.zone.activate(domain_name='example.com')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "status": "Success",
                "status_description":
                    "The zone was activated!"
            }
        }

    >>> cloudns_api.zone.deactivate(domain_name='example.com')

    >>> cloudns_api.zone.toggle_activation(domain_name='example.com')


Deleting a DNS Zone
^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.zone.delete(domain_name='example.com')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "status": "Success",
                "status_description":
                    "Domain zone example.com was deleted successfully."
            }
        }


Getting ClouDNS Zone Stats
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.zone.get_stats()

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "count": "25",  # Number of zones used
                "limit": "40"   # Number of zones allowed by your plan
            }
        }


Check if DNSSEC is available for a zone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.zone.dnssec_available(domain_name='example.com')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      1,
        }


Activating/Deactivating a DNSSEC
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.zone.dnssec_activate(domain_name='example.com')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "status": "Success",
                "status_description":
                    "The DNSSEC is activated for your zone. The keys will be generated soon."
            }
        }

    >>> cloudns_api.zone.deactivate(domain_name='example.com')


Getting DNSSEC DS Records
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.zone.dnssec_ds_records(domain_name='example.com')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
             "payload": {
                "status": "1",
                "ds": [
                    "example.com. 3600 IN DS 9813 13 2 613FDE9D90DB360EE4DDC1E18170D3306147A95E4F77177017C83E31057B9141"
                ],
                "ds_records": [
                    {
                        "digest": "613FDE9D90DB360EE4DDC1E18170D3306147A95E4F77177017C83E31057B9141",
                        "key_tag": "9813",
                        "algorithm": "13",
                        "algorithm_name": "ECDSA SHA-256",
                        "digest_type": "2",
                        "digest_type_name": "SHA-256"
                    }
                ],
                "dnskey": [
                    "example.com. 3600 IN DNSKEY 257 3 13 tDYgHxnS3cbLb9B2B2l+SsawWiG4jOzoFmnjy7PVL0NK5qiil/254sZLxEhXs0LNiL6YxcRVzYdHLkWi074SuQ==",
                    "example.com. 3600 IN DNSKEY 256 3 13 Nr9P1PdBNRCI7mpF7Nrx72rNZ7EQcHlVggUBJR0E9l+W0j37WlpluKM4qv/WVn/QsZxQOU1eSMPPyIXlT3sCvw=="
                ]
            }
        }


Checking if a DNS Zone Has Been Updated on all Servers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.zone.is_updated(domain_name='example.com')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      True
        }


SOA Record
----------

Every domain zone contains one SOA record that contains the current version of
the data in the zone, the administrator of the zone record, and TTL information
for the zone.

These functions only work for master zones.

SOA Parameters:

+ domain_name - string (required) Domain name or reverse zone name whose SOA
  details you want to modify.
+ primary_ns - string (required) Hostname of primary nameserver.
+ admin_mail - string (required) DNS zone administrator's e-mail.
+ refresh - integer (required) The time in seconds that a secondary DNS server
  waits before querying the primary DNS server's SOA record to check for
  changes. Rate can be any integer from 1200 to 43200 seconds.
+ retry - integer (required) The time in seconds that a secondary server waits
  before retrying a failed zone transfer. Usually, the retry rate is less than
  the refresh rate. Rate can be any integer from 180 to 2419200 seconds.
+ expire - integer (required) The time in seconds that a secondary server will
  keep trying to complete a zone transfer. If this time expires before a
  successful zone transfer, the secondary server will expire its zone file. The
  secondary will stop answering queries, as it considers its data too old to be
  reliable. Time can be any integer from 1209600 to 2419200 seconds.
+ default_ttl - integer (required) The minimum time-to-live value applies to
  all resource records in the zone file. TTL can be any integer from 60 to
  2419200 seconds.

Note that ClouDNS automatically increments the serial number when the zone is
updated or changed.


Getting the SOA for a domain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.soa.get('example.com')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "admin_mail":     "admin@example.com",
                "default_ttl":    "3600",
                "expire":         "1209600",
                "primary_ns":     "ns1.example.com",
                "refresh":        "7200",
                "retry":          "1800",
                "serial_number":  "2019060601"
            }
        }


Updating the SOA for a domain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.soa.update(
            'example.com',  # The domain to patch
            admin_mail='admin@example.com',
            default_ttl=3600,
            expire=1209600,
            primary_ns='ns1.example.com',
            refresh=7200,
            retry=1800,
        )

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "status": "Success",
                "status_description":
                    "The SOA record was modified successfully."
            }
        }


Patch Updating the SOA for a domain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A patch update allows you to specify only the parameters you wish to change.

.. code:: python

    >>> response = cloudns_api.soa.patch(
            'example.com',  # The domain to patch
            admin_mail='admin@example.com',
            primary_ns='ns1.example.com',
        )

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "status": "Success",
                "status_description":
                    "The SOA record was modified successfully."
            }
        }


DNS Records
-----------

Besides the SOA record, a domain can have a number of other records.

+ A record - points a hostname to an IPv4 address.

  * host - subdomain to optionally add to main domain

  * record - an IPv4

  * ttl - time to keep record in cache


+ AAAA record - points a hostname to an IPv6 address.

  * host - subdomain to optionally add to main domain

  * record - an IPv6

  * ttl - time to keep record in cache


+ MX record - server responsible for accepting e-mail messages.

  * host - subdomain to optionally add to main domain

  * record - hostname of the server that will handle the email messages

  * priority - priority index, prioritize the lowest indexed server

  * ttl - time to keep record in cache


+ CNAME record - canonical name record used for specifying host alisases.

  * host - subdomain to optionally add to main domain

  * record - the host this is an alias for

  * ttl - time to keep record in cache


+ TXT record - used to provide information for a wide variety of sources.

  * host - subdomain to optionally add to main domain

  * record - any text is valid

  * ttl - time to keep record in cache


+ SPF record - used to identify which servers are permitted to send emails for
  your host. This record type is deprecated in favor of using a TXT record.

  * host - subdomain to optionally add to main domain

  * record - a specific format is required for this record

  * ttl - time to keep record in cache


+ NS record - used to identify the name servers responsible for your domain.
  This must be the same as what your domain provider has configured.

  * host - subdomain to optionally add to main domain

  * record - the hostname of the nameserver

  * ttl - time to keep record in cache


+ SRV record - used to identify the host and port of specific services.

  * host - subdomain to optionally add to main domain

  * record - the hostname of the server

  * port - the port the service answers on

  * priority - priority index, prioritize the lowest indexed server

  * weight - a relative weight for services with the same index

  * ttl - time to keep record in cache


+ WR record - web redirect record. Points web requests from one server to
  another. This is not an official DNS record type.

  * host - subdomain to optionally add to main domain

  * record - the url to redirect

  * redirect-type - use a 301 (permanent) or 302 (temporary) redirect code

  * ttl - time to keep record in cache

  * frame - redirect the url in a frame so it is "transparent" to the user. Use
    '1' to enable and '0' to disable.

  * frame-title - Title of the frame

  * frame-keywords - Keywords used in the frame

  * frame-description - Description used in the frame


+ ALIAS record - a special ClouDNS record type similar to CNAME records that
  allow you to take advantage of Round-robbin DNS.

  * host - subdomain to optionally add to main domain

  * record - the host this is an alias for

  * ttl - time to keep record in cache


+ RP record - specifies the email address of the user responsible for the
  hostname.

  * host - subdomain to optionally add to main domain

  * record - an email address

  * ttl - time to keep record in cache


+ SSHFP record - contains the fingerprints for public keys used in SSH servers.

  * host - subdomain to optionally add to main domain

  * record - the fingerprint

  * algorithm - algorithm type to use (RSA, DSA, ECDSA, or Ed25159)

  * fptype - fingerprint type (SHA-1 or SHA-256)

  * ttl - time to keep record in cache


+ PTR record - used for reverse DNS lookups. For every PTR record, there must
  be a corresponding A record. Must be created on a reverse DNS zone.

  * host - subdomain to optionally add to main domain

  * record - the PTR record

  * ttl - time to keep record in cache


+ NAPTR record - used to map servers and user addresses in the Session
  Initiation Protocol (SIP)

  * host - subdomain to optionally add to main domain

  * record - the NAPTR record

  * ttl - time to keep record in cache


+ CAA record - allows a DNS domain name holder to specify one or more
  Certification Authorities (CAs) authorized to issue certificates for that
  domain

  * host - subdomain to optionally add to main domain

  * ttl - time to keep record in cache

  * caa-flag - 0 for non-critical, 128 for critical

  * caa-type - issue, issuewild, iodef

  * caa-value - the record value


+ TLSA record - asociates a TLS certificate or public key with the domain name

  * host - the RFC TLSA format: _port._protocol.host.domain.com. (example:
    _80._tcp.host.example.com)

  * tlsa_usage - an integer with one of the following values:

    - 0 - PKIX-TA: Certificate Authority Constraint

    - 1 - PKIX-EE: Service Certificate Constraint

    - 2 - DANE-TA: Trust Anchor Assertion

    - 3 - DANE-EE: Domain Issued Certificate

  * tlsa_selector - an integer with one of the following values:

    - 0 - Cert: Use full certificates

    - 1 - SPKI: Use subject public key

  * tlsa_matching_type - an integer with one of the following values:

    - 0 - Full: No Hash

    - 1 - SHA-256: SHA-256 Hash

    - 2 - SHA-512: SHA-512 hash

  * record - the certificate association data in hexedecimal format

  * ttl - time to keep record in cache


A wildcard ('*') can be added for domains and subdomains that do not exist in
the DNS record for these types: A (or AAAA), MX, TXT, CNAME, ALIAS and Web
Redirect.

ClouDNS supports the following values for TTLs:

+ 1 Minute
+ 5 Minutes
+ 15 Minutes
+ 30 Minutes
+ 1 Hours
+ 6 Hours
+ 12 Hours
+ 1 Day
+ 2 Days
+ 3 Days
+ 1 Week
+ 2 Weeks
+ 1 Month

ClouDNS uses round-robbin DNS when multiple A, AAAA, or Alias records are
provided with different values.


Getting available record types for a zone
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.record \
            .get_available_record_types(zone_type='domain')

    >>> print(response.json())


        {
            "success":      True,
            "status_code":  200,
            "payload":      [
                "A", "AAAA", "MX", "CNAME", "TXT", "SPF", "NS", "SRV", "WR",
                "ALIAS", "RP", "SSHFP", "NAPTR", "CAA"
            ]
        }


Getting available TTLs for Records
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.record.get_available_ttls()

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      [
                60, 300, 900, 1800, 3600, 21600, 43200, 86400, 172800, 259200,
                604800, 1209600, 2592000
            ]
        }


Listing DNS Records
^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.record.list(domain_name='example.com',
                                           host='ns1')  # Host is optional
    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "1234567": {
                    "id":                "1234567",
                    "type":              "A",
                    "host":              "ns1",
                    "record":            "10.0.0.1",
                    "dynamicurl_status": 0,
                    "failover":          "0",
                    "ttl":               "86400",
                    "status":            1
                },
                "2345678": {
                    "id":                "2345678",
                    "type":              "A",
                    "host":              "ns1",
                    "record":            "10.0.0.2",
                    "dynamicurl_status": 0,
                    "failover":          "0",
                    "ttl":               "86400",
                    "status":            1
                }
            }
        }


Creating DNS Records
^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.record.create(domain_name='example.com',
                                             host='', record_type='A',
                                             record='10.10.10.10', ttl=3600)

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "status": "Success",
                "status_description": "The record was added successfully.",
                "data": {"id": 123456789}
            }
        }


Transferring DNS Records
^^^^^^^^^^^^^^^^^^^^^^^^

NOTE: This currently doesn't work as expected. For every domain, I seem to be
getting 'The zone transfers are not allowed from this server!'

.. code:: python

    >>> response = cloudns_api.record.transfer(domain_name='example.com',
                                               server='1.1.1.1')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {}
        }


Copying DNS Records
^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.record.copy(domain_name='example.com',
                                           from_domain='example.net',
                                           delete_current_records=False)

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "status": "Success",
                "status_description": "8 records were copied",
            }
        }


Getting a specific DNS Record
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.record.get(domain_name='example.com',
                                          record_id=1234567)

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "id":                "1234567",
                "type":              "A",
                "host":              "ns1",
                "record":            "10.0.0.1",
                "dynamicurl_status": 0,
                "failover":          "0",
                "ttl":               "86400",
                "status":            1
            }
        }


Exporting a DNS Record to BIND
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.record.export(domain_name='example.com')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "status": "Success",
                "zone": "$ORIGIN example.com.\n@\t3600\tIN\tSOA\tns1.example.com. ...."
            }
        }


Getting the Dynamic URL for a DNS Record
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.record.get_dynamic_url(
            domain_name='example.com', record_id='12345')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "host":              "example.com",
                "url":               "https://ipv4.cloudns.net/api/dynamicURL/?q=ABC123",
            }
        }

        # This will set 'example.com' to the IP address of the machine that
        # runs the code:
    >>> requests.get('https://ipv4.cloudns.net/api/dynamicURL/?q=ABC123')

        OK


Updating a specific DNS Record
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.record.get(domain_name='example.com',
                                          record_id=1234567)

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload": {
                "id":                "1234567",
                "type":              "A",
                "host":              "",
                "record":            "10.0.0.1",
                "dynamicurl_status": 0,
                "failover":          "0",
                "ttl":               "86400",
                "status":            1
            }
        }


Activating/Deactivating a DNS Record
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.record.activate(domain_name='example.com')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "status": "Success",
                "status_description":
                    "Record activated"
            }
        }

    >>> cloudns_api.record.deactivate(domain_name='example.com')

    >>> cloudns_api.record.toggle_activation(domain_name='example.com')


Deleting a specific DNS Record
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.record.delete(domain_name='example.com',
                                             record_id='123456789')

    >>> print(response.json())

        {
            "success":      True,
            "status_code":  200,
            "payload":      {
                "status": "Success",
                "status_description": "The record was deleted successfully.",
            }
        }

Soli Deo gloria.
