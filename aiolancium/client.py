from .auth import Authenticator
from .decorator import AuthDecorator, ResponseDecorator
from .proxy import ApiProxy
from .utilities.utilities import upload_helper

from typing import Optional


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

    async def upload_image_helper(
        self, path, source, name, source_type="singularity_image", chunk_size=32000000
    ):
        await upload_helper(
            awaitable_create_method=self.images.create_image,
            awaitable_upload_method=self.images.upload_image_file,
            path=path,
            source=source,
            source_type=source_type,
            chunk_size=chunk_size,
            name=name,
        )

    async def upload_file_helper(self, path, source, force=True, chunk_size=32000000):
        await upload_helper(
            awaitable_create_method=self.data.create_data_item,
            awaitable_upload_method=self.data.upload_data_file,
            path=path,
            source=source,
            source_type="file",
            chunk_size=chunk_size,
            force=force,
        )
