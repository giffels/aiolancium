from .auth import Authenticator
from .decorator import AuthDecorator, ResponseDecorator
from .proxy import ApiProxy
from .utilities.utilities import read_binary_chunks_from_file

from typing import Optional

import os


class LanciumClient(object):
    def __init__(self, api_url: str, auth: Authenticator, timeout: int = 60) -> None:
        self.api_url = api_url
        self.auth = auth
        self.api_proxy = ApiProxy(api_url=api_url, timeout=timeout)

    def __getattr__(self, item):
        return AuthDecorator(
            ResponseDecorator(getattr(self.api_proxy, item)), self.auth
        )

    async def download_file_helper(
        self, path: str, destination: str, job_id: Optional[int] = None
    ):
        if job_id:
            # job output returned as string, needs to be converted into bytes first
            content = (await self.jobs.download_job_output(job_id, path)).encode()
        else:
            content = await self.data.get_data(path)

        with open(destination, "wb") as f:
            f.write(content)

    async def upload_file_helper(self, path, source, force=True, chunk_size=32000000):
        file_size = os.path.getsize(source)

        await self.data.create_data_item(
            path=path, source_type="file", source=source, size=file_size, force=force
        )

        for chunk_data in read_binary_chunks_from_file(
            file_name=source, chunk_size=chunk_size
        ):
            await self.data.upload_data_file(path, **chunk_data)
