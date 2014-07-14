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
- beautifulsoup


Installation
------------

.. code-block:: bash

    $ pip install python-zanox-api


Example
-------

.. code-block:: python

    >>> from zanox import PublisherApi
    >>> api = PublisherApi(connect_id=XXXXX, secret_key=XXXXX)
    >>> example1 = api.get('programs')
    >>> example2 = api.get('programs', start_date='2012-01-01')
    >>> example3 = api.get('programs/program/1234')
    >>> example4 = api.get_tracking_url('http://www.example.com/foo/bar.html', adspace=XXXXX)
    ...


TODOs and BUGS
==============

See: http://github.com/baskoopmans/python-zanox-api/