from .auth import Authenticator
from .proxy import ApiProxy
from .resources import lancium_resources
from .utilities.utilities import read_binary_chunks_from_file

from simple_rest_client.api import API

import os


class LanciumClient(object):
    def __init__(self, api_url: str, auth: Authenticator, timeout: int = 60) -> None:
        self.api_url = api_url

        self.api_proxy = ApiProxy(
            api=API(
                api_root_url=self.api_url,
                json_encode_body=False,
                headers={
                    "Accept": "application/json",
                },
                timeout=timeout,
            ),
            auth=auth,
        )

        for resource in lancium_resources:
            self.api_proxy.add_resource(**resource)

    def __getattr__(self, item):
        return getattr(self.api_proxy, item)

    async def upload_file_helper(self, path, source, force=True, chunk_size=32000000):
        file_size = os.path.getsize(source)

        await self.data.create_data_item(
            path=path, source_type="file", source=source, size=file_size, force=force
        )

        for chunk_data in read_binary_chunks_from_file(
            file_name=source, chunk_size=chunk_size
        ):
            await self.data.upload_data_file(path, **chunk_data)
