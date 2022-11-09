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

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
