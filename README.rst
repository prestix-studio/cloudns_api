cloudns_api
###########

A python interface to the ClouDNS.net API
=========================================

Please note that this is still in Beta. Use at your own risk.

This project is an independent project not developed by
`CloudNS.net <https://cloudns.net>`__.

The interface is designed to be simple and intuitive. Entities are represented
as modules and there is a simple list, create, update, and delete function
(when appropriate, ie, you cannot delete an SOA record) for each entity. Some
entities have functions specific to them, but whenever possible, the arguments
are consistent. The code reads pretty clearly.

For information on the `CloudNS.net <https://cloudns.net>`__ API see `here
<https://www.cloudns.net/wiki/article/41/>`__.

Please submit any bug reports and bug fixes on github `here
<https://github.com/hbradleyiii/>`__.



Installing and including in projects
====================================


Installing cloudns_api
----------------------

.. code:: bash

    $ pip install cloudns_api


In order to authenticate correctly, create the following environment variables
(using your own credentials):

.. code:: bash

    export CLOUDNS_API_AUTH_USER=my_user
    export CLOUDNS_API_AUTH_PASSWORD=my_password

    # When you are debugging:
    export CLOUDNS_API_DEBUG=True


To make things easier, you could put these in your python virtual environment
or use a package like
`python-dotenv <https://github.com/theskumar/python-dotenv>`__ to automatically
load your environment variables. Be sure to not include your private username
and password in your public repositories.


Running Tests
-------------

.. code:: bash

    $ cd <cloudns_api directory>
    $ py.test


Importing and Basic Usage
-------------------------

.. code:: python

    >>> import cloudns_api

    >>> response = cloudns_api.zone.list(search='example')

    >>> print(response.json())

        {
            'success':      True,
            'status_code':  200,
            'payload':      [
                {
                    'name':     'example.com',
                    'type':     'master',
                    'zone':     'domain',
                    'status':   '1'
                },
                {
                    'name':     'example.net',
                    'type':     'master',
                    'zone':     'domain',
                    'status':   '1'
                },
                {
                    'name':     'example.org',
                    'type':     'master',
                    'zone':     'domain',
                    'status':   '1'
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

The ClouDNS sometimes uses camel case and sometimes uses dashes in its
parameters. In our API, we convert both of these to snake case for consistency
and compatibility with python.

API update functions require all required parameters to be passed. This can be
inconvenient at times, so cloudns_api includes an argument `patch` that when
set to True allows you to only pass arguments you wish to change. Behind the
scenes, the API will get the existing data and merge it with the new data for
the update call. We've also included the convenient `patch` function as a
wrapper around `update` with the `patch` argument set to True.

The cloudns_api includes these two helpful functions for checking your login
credentials and retrieving your CloudNS nameservers:

.. code:: python

    >>> print(cloudns_api.api.get_login())

        {
            'success':      True,
            'status_code':  200,
            'payload':      {
                'status':             'Success',
                'status_description': 'Success login.'
            }
        }

    >>> print(cloudns_api.api.get_nameservers())


ApiResponse
^^^^^^^^^^^

All API calls return an ApiResponse instance. The `ApiResponse` object is a
wrapper object to add custom functionality and properties to a basic response
object from the `requests <https://github.com/kennethreitz/requests>`__
library.

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

The ApiParameter object is responsible for describing the kinds of parameters
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


DNS SOA Record
--------------

Every domain zone contains one SOA record that contains the current version of
the data in the zone, the administrator of the zone record, and TTL information
for the zone.

These functions only work for master zones.


Getting the SOA for a domain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    >>> response = cloudns_api.soa.get('example.com')
    >>> print(response.json())

        {
            'success':      True,
            'status_code':  200,
            'payload':      {
                'admin_mail':     'admin@example.com',
                'default_ttl':    '3600',
                'expire':         '1209600',
                'primary_ns':     'ns1.example.com',
                'refresh':        '7200',
                'retry':          '1800',
                'serial_number':  '2019060601'},
            }
        }


Updating the SOA for a domain
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Parameters:

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


.. code:: python

    >>> response = cloudns_api.soa.update(
            'example.com',  # The domain to patch
            admin_mail='admin@example.com',
            default_ttl=3600,
            expire=1209600,
            primary_ns='ns1.example.com',
            refresh=7200,
            retry=1800,
        })

    >>> print(response.json())

        {
            'success':      True,
            'status_code':  200,
            'payload':      {
                'status': 'Success',
                'status_description':
                    'The SOA record was modified successfully.'
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
            'success':      True,
            'status_code':  200,
            'payload':      {
                'status': 'Success',
                'status_description':
                    'The SOA record was modified successfully.'
            }
        }



Soli Deo gloria.
