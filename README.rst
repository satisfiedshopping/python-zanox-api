====================
Python Zanox API
====================
Python zanox.com API - A simple Python wrapper around the zanox.com developer API
Publisher API - https://developer.zanox.com/web/guest/publisher-api-2011


Dependencies
============
- beautifulsoup


Installation
============
pip install python-zanox-api


Example
=============
```python
from zanox import PublisherApi
api = PublisherApi(connect_id=XXXXX, secret_key=XXXXX)
example1 = api.get('programs')
example2 = api.get('programs', start_date='2012-01-01')
example3 = api.get('programs/program/1234')
```

TODOs and BUGS
==============
See: http://github.com/baskoopmans/python-zanox-api/