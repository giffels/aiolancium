[![Build Status](https://github.com/giffels/aiolancium/actions/workflows/unittests.yaml/badge.svg)](https://github.com/giffels/aiolancium/actions/workflows/unittests.yaml)
[![Verification](https://github.com/giffels/aiolancium/actions/workflows/verification.yaml/badge.svg)](https://github.com/giffels/aiolancium/actions/workflows/verification.yaml)
[![codecov](https://codecov.io/gh/giffels/aiolancium/branch/main/graph/badge.svg)](https://codecov.io/gh/giffels/aiolancium)
[![Documentation Status](https://readthedocs.org/projects/aiolancium/badge/?version=latest)](https://aiolancium.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/aiolancium.svg)](https://badge.fury.io/py/aiolancium)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/aiolancium.svg?style=flat-square)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/giffels/aiolancium/blob/master/LICENSE)
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# aiolancium

aiolancium is a simplistic python REST client for the Lancium Compute REST API utilizing asyncio. The client itself has
been developed against the [Lancium Compute REST API documentation](https://lancium.github.io/compute-api-docs/api.html).

## Installation
aiolancium can be installed via [PyPi](https://pypi.org/) using

```bash
pip install aiolancium
```

## How to use aiolancium

```python
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
```

In order to simplify file uploads and downloads to/from the Lancium compute platform, an upload/download helper method 
has been added to the client. 
The upload helper takes care of reading a file in binary format and uploading it in 32 MB chunks (default) to the 
Lancium persistent storage. The download helper downloads a file from the Lancium persistent storage to the local disks.
The download helper also supports the download of jobs outputs (stdout.txt, stderr.txt) to local disk (see example 
above).
Unfortunately, streaming of data is not support by the underlying `simple-rest-client`. Thus, the entire file is 
downloaded to memory before writing to the disk.

```python
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

# Download the file again
await client.download_file_helper("/test", destination="test_downloaded_again")

# Delete the uploaded file again, the 
arg = {"file-path": "/test"}
await client.data.delete_data_item(**arg)

# Alternative approach to delete the uploaded file
await client.data.delete_data_item("/test")
```
