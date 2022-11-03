from .auth import Authenticator
from .proxy import ApiProxy
from .resources import lancium_resources

from simple_rest_client.api import API


class LanciumClient(object):
    def __init__(self, api_url: str, auth: Authenticator, timeout: int = 60) -> None:
        self.api_url = api_url

        self.api_proxy = ApiProxy(
            api=API(
                api_root_url=self.api_url,
                json_encode_body=True,
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json",
                },
                timeout=timeout,
            ),
            auth=auth,
        )

        for resource in lancium_resources:
            self.api_proxy.add_resource(**resource)

    def __getattr__(self, item):
        return getattr(self.api_proxy, item)
