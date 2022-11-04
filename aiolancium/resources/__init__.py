from .openapi import OpenApiParser

from simple_rest_client.resource import AsyncResource

import os


lancium_resources = []

parser = OpenApiParser(f"{os.path.dirname(os.path.realpath(__file__))}/api.json")

for resource_group, actions in parser.get_actions().items():
    resource_class = type(
        f"Lancium{resource_group.capitalize()}Resource", (AsyncResource,), actions
    )
    lancium_resources.append(
        dict(resource_name=resource_group, resource_class=resource_class)
    )

__all__ = ["lancium_resources"]
