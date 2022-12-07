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

   changelog
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

Dealing with Jobs
^^^^^^^^^^^^^^^^^

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

   for job in jobs["jobs"]:
       # Retrieve the stdout/stdin output of your finished jobs
       await client.jobs.download_job_output(job["id"], "stdout.txt")
       await client.jobs.download_job_output(job["id"], "stderr.txt")

       # or download them to disk
       await client.download_file_helper("stdout.txt", "stdout.txt", job["id"])
       await client.download_file_helper("stderr.txt", "stderr.txt", job["id"])

   # Delete all your jobs in Lancium compute
   for job in jobs["jobs"]:
    await client.jobs.delete_job(id=job["id"])


File uploads/downloads to/from the Lancium compute persistent storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In order to simplify file uploads and downloads to/from the Lancium compute platform, an upload/download helper method
has been added to the client.

The upload helper takes care of reading a file in binary format and uploading it in 32 MB chunks (default) to the
Lancium persistent storage. The download helper downloads a file from the Lancium persistent storage to the local disks.

The download helper also supports the download of jobs outputs (stdout.txt, stderr.txt) to local disk (see example
above). Unfortunately, streaming of data is not support by the underlying `simple-rest-client`. Thus, the entire file is
downloaded to memory before writing to the disk.

Depending on the internet connection and the chunk/file size, it can be reasonable to adjust the timeout parameter of
the `LanciumClient`.

.. code-block:: python

   from aiolancium.auth import Authenticator
   from aiolancium.client import LanciumClient

   # Authenticate yourself against the API and refresh your token if necessary
   auth = Authenticator(api_key="<your_api_key>")

   # Initialise the actual client
   client = LanciumClient(api_url="https://portal.lancium.com/api/v1/", auth=auth, timeout=300)

   # Upload /bin/bash to /test on the Lancium persistent storage
   await client.upload_file_helper(path="test", source="/bin/bash")

   # Get information about the uploaded file
   await client.data.get_file_info("/test")

   # Download the file again
   await client.download_file_helper("/test", destination="test_downloaded_again")

   # Delete the uploaded file again, the
   arg = {"file-path": "/test"}
   await client.data.delete_data_item(**arg)

   # Alternative approach to delete the uploaded file
   await client.data.delete_data_item("/test")

Image uploads to the Lancium compute persistent storage
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to simplify image uploads to the Lancium compute platform, an upload image helper method
has been added to the client.
The upload helper takes care of reading a image in binary format and uploading it in 32 MB chunks (default) to the
Lancium persistent storage.

Depending on the internet connection and the chunk size, it can be reasonable to adjust the
timeout parameter of the `LanciumClient`.

.. code-block:: python

   from aiolancium.auth import Authenticator
   from aiolancium.client import LanciumClient

   # Authenticate yourself against the API and refresh your token if necessary
   auth = Authenticator(api_key="<your_api_key>")

   # Initialise the actual client
   client = LanciumClient(api_url="https://portal.lancium.com/api/v1/", auth=auth, timeout=300)

   # Upload rockylinux8 to matterminers/rockylinux8 on the Lancium persistent storage
   await client.upload_image_helper(path="matterminers/rockylinux8", name="rockylinux8",
                                    source="rockylinux8.sif", source_type="singularity_image")

   # Get information about the uploaded image incl. the status of it. Only image with status ready can be used
   await client.images.list_image("matterminers/rockylinux8")

   # Delete an image on the Lancium platform
   await client.images.delete_image("matterminers/rockylinux8")

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
