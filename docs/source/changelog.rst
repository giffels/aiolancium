.. Created by changelog.py at 2022-11-30, command
   '/Users/giffler/.cache/pre-commit/repor6pnmwlm/py_env-python3.10/bin/changelog docs/source/changes compile --output=docs/source/changelog.rst'
   based on the format of 'https://keepachangelog.com/'

#########
CHANGELOG
#########

[Unreleased] - 2022-11-30
=========================

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
