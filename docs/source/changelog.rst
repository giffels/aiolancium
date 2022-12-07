.. Created by changelog.py at 2022-12-07, command
   '/Users/giffler/.cache/pre-commit/repor6pnmwlm/py_env-python3.10/bin/changelog docs/source/changes compile --output=docs/source/changelog.rst'
   based on the format of 'https://keepachangelog.com/'

#########
CHANGELOG
#########

[Unreleased] - 2022-12-07
=========================

Fixed
-----

* Fixed typo in the checksum header and wrong format of the upload body

[0.2.1] - 2022-12-01
====================

Fixed
-----

* Do not verify the audience claim of the auth token

[0.2.0] - 2022-11-30
====================

Added
-----

* Added support for get_file_info API call
* Added file download helper and support for asynchronous downloads
* Add upload file helper to simplify file uploads

Changed
-------

* Extract token expiry date from token itself
* Automatically encode method bodies according to content-type in open api

Fixed
-----

* Url encode the query parameters
