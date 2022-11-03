import jsonref
import re


class OpenApiParser(object):
    def __init__(self, filename):
        self.in_path_pattern = re.compile(r"{(.*?)}")
        with open(filename, "r") as f:
            self.open_api = jsonref.load(f)

    def get_actions(self):
        resources = {}
        for path in self.paths:
            resource_group = self.get_resource_group(path)
            for method in self.get_methods(path):
                resources.setdefault(resource_group, {}).setdefault(
                    "actions", {}
                ).update(
                    {
                        self.get_operation_id(path, method): {
                            "url": self.get_substituted_path(path),
                            "method": method.upper(),
                            "parameters": [],  # self.get_parameters(path, method),
                        }
                    }
                )
        # ToDo Eventuell aufsplitten in verschiedene Funktionen
        return resources

    @property
    def paths(self):
        return self.open_api["paths"].keys()

    def get_methods(self, path):
        return self.open_api["paths"][path].keys()

    def get_method_detail(self, path, method, detail):
        return self.open_api["paths"][path][method][detail]

    def get_operation_id(self, path, method):
        return self.get_method_detail(path, method, "operationId")

    def get_parameters(self, path, method):
        try:
            if method == "list_image":
                print("openapi", self.get_method_detail(path, method, "parameters"))
                # ToDo: Parse in-path and header parameters
            return self.get_method_detail(path, method, "parameters")
        except KeyError:
            return []

    def get_content_type(self, path, method):
        for key in self.get_method_detail(path, method, "requestBody")["content"]:
            return key

    @staticmethod
    def get_resource_group(path):
        return path.split("/")[1]

    def get_substituted_path(self, path):
        return self.in_path_pattern.sub("{}", path)
