from .auth import Authenticator
from .interfaces import ProxyDecorator, Proxy

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
    async def __call__(self, awaitable_method: Callable, *args, **kwargs):
        result = await awaitable_method(*args, **kwargs)
        return result.body
