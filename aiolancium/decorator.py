from .auth import Authenticator
from .interfaces import ProxyDecorator, Proxy
from .utilities.utilities import extract_kwargs, get_method_name

from typing import Callable


class AuthDecorator(ProxyDecorator):
    def __init__(self, proxy: Proxy, auth: Authenticator):
        super().__init__(proxy)
        self.auth = auth

    async def __call__(self, awaitable_method: Callable, *args, **kwargs):
        kwargs.setdefault("headers", {}).update(
            {"Authorization": await self.auth.get_token()}
        )
        return await awaitable_method(*args, **kwargs)


class ResponseDecorator(ProxyDecorator):
    _file_info_kwargs = (
        "X-Object-Type",
        "X-Last-Modified",
        "X-Date-Created",
        "X-File-Size",
    )

    async def __call__(self, awaitable_method: Callable, *args, **kwargs):
        result = await awaitable_method(*args, **kwargs)
        # get_file_info is the only function where data is returned via the header
        if get_method_name(awaitable_method) == "get_file_info":
            return extract_kwargs(self._file_info_kwargs, result.headers)
        return result.body
