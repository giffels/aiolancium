from .interfaces import Proxy
from .resources import lancium_resources
from .utilities.utilities import extract_kwargs

from simple_rest_client.api import API
from simple_rest_client.resource import BaseResource
from simple_rest_client.resource import AsyncResource

from functools import partial
from inspect import signature
from urllib.parse import quote_plus
from typing import Dict

import json


class ApiProxy(Proxy):
    def __init__(self, api_url: str, timeout: int):
        self.api = API(
            api_root_url=api_url,
            json_encode_body=False,
            headers={
                "Accept": "application/json",
            },
            timeout=timeout,
        )

        for resource in lancium_resources:
            self.api.add_resource(**resource)

    def __call__(self, method_name: str, *args, **kwargs):
        raise TypeError(f"{self.__class__.__name__} object is not callable!")

    def __getattr__(self, item):
        return ResourceProxy(resource=getattr(self.api, item))


class ResourceProxy(Proxy):
    pass_through_kwargs = [
        arg for arg in signature(BaseResource.__init__).parameters if arg != "self"
    ]

    def __init__(self, resource: AsyncResource) -> None:
        self.resource = resource

    async def __call__(self, method_name: str, *args, **kwargs):
        # Split keyword arguments into pass through arguments the `BaseResource` object
        # is expecting, the parameters the API is expecting and put anything else into
        # the body of the API call
        header_parameters = extract_kwargs(
            self.resource.actions.get(method_name)["parameters"].get("header", []),
            kwargs,
        )
        content_type = self.resource.actions.get(method_name)["content-type"]
        for header_parameter in (header_parameters, content_type):
            kwargs.setdefault("headers", {}).update(header_parameter)

        query_parameters = self.query_param_encode(
            extract_kwargs(
                self.resource.actions.get(method_name)["parameters"].get("query", []),
                kwargs,
            )
        )
        kwargs.setdefault("params", {}).update(query_parameters)

        path_parameters = extract_kwargs(
            self.resource.actions.get(method_name)["parameters"].get("path", []), kwargs
        )

        pass_through_kwargs = extract_kwargs(self.pass_through_kwargs, kwargs)

        # Check if there is a dedicated body keyword argument, otherwise consider
        # all other keyword arguments as method body and encode it properly
        body = kwargs.get("body", kwargs)

        if body and content_type["Content-Type"] == "application/json":
            # JSON encode body if content type is application/json
            body = json.dumps(body)

        awaitable_method = getattr(self.resource, method_name)
        return await awaitable_method(
            *args, *(path_parameters.values()), **pass_through_kwargs, body=body
        )

    def __getattr__(self, method_name: str):
        return partial(self, method_name)

    @staticmethod
    def query_param_encode(parameters: Dict) -> Dict:
        return {key: quote_plus(value) for key, value in parameters.items()}
