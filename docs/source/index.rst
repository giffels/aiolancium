.. aiolancium documentation master file, created by
   sphinx-quickstart on Mon Aug  5 10:26:52 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to aiolancium's documentation!
======================================

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Contents:

   Module Index <api/modules>

aiolancium
==========

aiolancium is a simplistic python REST client for the Lancium Compute REST API utilizing asyncio.
The client itself has been developed against the
`Lancium Compute REST API documentation <https://lancium.github.io/compute-api-docs/api.html>`_.

Installation
------------
aiolancium can be installed via `PyPi <https://pypi.org/)>`_ using

.. code-block:: bash

   pip install aiolancium


How to use aiolancium
---------------------

.. code-block:: python

   from aiolancium.auth import Authenticator
   from aiolancium.client import LanciumClient

   # Authenticate yourself against the API and refresh your token if necessary
   auth = Authenticator(api_key="<your_api_key>")

   # Initialise the actual client
   client = LanciumClient(api_url="https://portal.lancium.com/api/v1/", auth=auth)

   # List details about the `lancium/ubuntu` container
   await client.images.list_image("lancium/ubuntu")

   # Create your hellow world first job.
   job = {"job": {"name": "GridKa Test Job",
                  "qos": "high",
                  "image": "lancium/ubuntu",
                  "command_line": 'echo "Hello World"',
                  "max_run_time": 600}}

   await client.jobs.create_job(**job)

   # Show all your jobs and their status in Lancium compute
   jobs = await client.jobs.show_jobs()

   # Delete all your jobs in Lancium compute
   for job in jobs["jobs"]:
    await client.jobs.delete_job(id=job["id"])


File uploads to the Lancium compute persistent storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In order to simplify file uploads to the Lancium compute platform, an upload helper method has been added to the client.
It takes care of reading a file in binary format and uploading it in 32 MB chunks (default) to the Lancium persistent
storage.

.. code-block:: python

   from aiolancium.auth import Authenticator
   from aiolancium.client import LanciumClient

   # Authenticate yourself against the API and refresh your token if necessary
   auth = Authenticator(api_key="<your_api_key>")

   # Initialise the actual client
   client = LanciumClient(api_url="https://portal.lancium.com/api/v1/", auth=auth)

   # Upload /bin/bash to /test on the Lancium persistent storage
   await client.upload_file_helper(path="test", source="/bin/bash")

   # Get information about the uploaded file
   await client.data.get_file_info("/test")

   # Delete the uploaded file again, the
   arg = {"file-path": "/test"}
   await client.data.delete_data_item(**arg)

   # Alternative approach to delete the uploaded file
   await client.data.delete_data_item("/test")

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
