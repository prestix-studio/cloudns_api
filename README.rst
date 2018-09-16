cloudns_api
####
A python interface to the ClouDNS.net API
===========================================================

Please note that this is still in Beta. Use at your own risk.

This project is an independent project and is not endorsed by
`CloudNS.net <https://cloudns.net>`_.

The interface is designed to be simple and intuitive. Entities are represented
as modules and there is a simple list, create, update, and delete function
(when appropriate, ie, you cannot delete an SOA record) for each entity. Some
entities have functions specific to them, but whenever possible, the arguments
are consistent. The code reads pretty clearly.

For information on the `CloudNS.net <https://cloudns.net>`_ API see `here
<https://www.cloudns.net/wiki/article/41/>`_.


Installing and including in projects
====================================

Installing cloudns_api
---------------

.. code:: bash

    $ pip install cloudns_api

In order to authenticate correctly, create the following environment variables
(using your own credentials):

.. code:: bash

    export CLOUDNS_AUTH_USER=my_user
    export CLOUDNS_AUTH_PASSWORD=my_password


Running Tests
-------------

.. code:: bash

    $ cd <project directory>
    $ py.test

Importing and Basic Usage
-------------------------

.. code:: python

    >>> import cloudns_api


----

Soli Deo gloria.
