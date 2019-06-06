cloudns_api: A python interface to the ClouDNS.net API
======================================================

Please note that this is still in Beta. Use at your own risk.

This project is an independent project and is not endorsed by
`CloudNS.net <https://cloudns.net>`__.

The interface is designed to be simple and intuitive. Entities are represented
as modules and there is a simple list, create, update, and delete function
(when appropriate, ie, you cannot delete an SOA record) for each entity. Some
entities have functions specific to them, but whenever possible, the arguments
are consistent. The code reads pretty clearly.

For information on the `CloudNS.net <https://cloudns.net>`__ API see `here
<https://www.cloudns.net/wiki/article/41/>`__.


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


Running Tests
-------------

.. code:: bash

    $ cd <project directory>
    $ py.test


Importing and Basic Usage
-------------------------

.. code:: python

    >>> import cloudns_api

    >>> response = cloudns_api.soa.get('example.com')
    >>> print(response.json())

        {
            'success'     : True,
            'status_code' : 200,
            'payload'     : {
                'admin_mail'    : 'admin@example.com',
                'default_ttl'   : '3600',
                'expire'        : '1209600',
                'primary_ns'    : 'ns1.example.com',
                'refresh'       : '7200',
                'retry'         : '1800',
                'serial_number' : '2019060601'},
            }
        }

    >>> cloudns_api.soa.update(
            'example.com',
            admin_mail='admin@example.com,
            default_ttl=3600,
            expire='1209600', # You can use strings or integers
            primary_ns='ns1.example.com',
            refresh=7200,
            retry=1800,
            serial_number=2019060601
        )


API Reference
-------------


----

Soli Deo gloria.
