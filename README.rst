Python Zanox API
================

Python zanox.com API - A simple Python wrapper around the zanox.com developer API

Publisher API - https://developer.zanox.com/web/guest/publisher-api-2011


Features
--------

- Easy to use wrapper
- Generate tracking url for deeplinks


Dependencies
------------

- requests
- xmltodict


Installation
------------

.. code-block:: bash

    $ pip install python-zanox-api


Example
-------

.. code-block:: python

    >>> from zanox.apis import PublisherApi
    >>> api = PublisherApi(connect_id='XXXXX', secret_key='XXXXX', from_email='yourmail@example.com')
    >>> example1 = api.get('programs')
    >>> example2 = api.get('programs', start_date='2012-01-01')
    >>> example3 = api.get('programs/program/1234')
    >>> example4 = api.get_tracking_url('http://www.example.com/foo/bar.html', adspace=XXXXX)
    ...

Parameters
----------

- **connect_id** Zanox Connect ID (mandatory)
- **secret_key** Zanox Secret Key (mandatory)
- **domain** default: api.zanox.com
- **format** default: json
- **version** default: 2011-03-01
- **ssl** default: True
- **user_agent** default: PythonZanoxApi/x.x.x
- **from_email** (optional)


TODOs and BUGS
==============

See: http://github.com/baskoopmans/python-zanox-api/