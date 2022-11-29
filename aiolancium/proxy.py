from .auth import Authenticator
from .decorator import AuthDecorator, ResponseDecorator
from .interfaces import Proxy

from simple_rest_client.api import API
from simple_rest_client.resource import BaseResource
from simple_rest_client.resource import AsyncResource

from functools import partial
from inspect import signature
from urllib.parse import quote_plus
from typing import Dict, Iterable

import json


class ApiProxy(Proxy):
    def __init__(self, api: API, auth: Authenticator):
        self.api = api
        self.auth = auth

    def add_resource(
        self,
        api_root_url=None,
        resource_name=None,
        resource_class=None,
        params=None,
        headers=None,
        timeout=None,
        append_slash=False,
        json_encode_body=False,
    ):
        return self.api.add_resource(
            api_root_url=api_root_url,
            resource_name=resource_name,
            resource_class=resource_class,
            params=params,
            headers=headers,
            timeout=timeout,
            append_slash=append_slash,
            json_encode_body=json_encode_body,
        )

    def __call__(self, method_name: str, *args, **kwargs):
        raise TypeError(f"{self.__class__.__name__} object is not callable!")

    def __getattr__(self, item):
        return AuthDecorator(
            ResponseDecorator((ResourceProxy(resource=getattr(self.api, item)))),
            auth=self.auth,
        )


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
        header_parameters = self.extract_kwargs(
            self.resource.actions.get(method_name)["parameters"].get("header", []),
            kwargs,
        )
        content_type = self.resource.actions.get(method_name)["content-type"]
        for header_parameter in (header_parameters, content_type):
            kwargs.setdefault("headers", {}).update(header_parameter)

        query_parameters = self.query_param_encode(
            self.extract_kwargs(
                self.resource.actions.get(method_name)["parameters"].get("query", []),
                kwargs,
            )
        )
        kwargs.setdefault("params", {}).update(query_parameters)

        path_parameters = self.extract_kwargs(
            self.resource.actions.get(method_name)["parameters"].get("path", []), kwargs
        )

        pass_through_kwargs = self.extract_kwargs(self.pass_through_kwargs, kwargs)

        # Consider all other keyword arguments as method body and encode it properly
        body = kwargs
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

    @staticmethod
    def extract_kwargs(keys: Iterable, kwargs):
        return {key: kwargs.pop(key) for key in keys if key in kwargs}
