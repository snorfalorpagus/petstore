from typing import Tuple, Dict, List, Optional, Any, Union
from inspect import signature
from pathlib import Path

import yaml
from connexion import Resolver
from connexion.lifecycle import ConnexionResponse

from dataclasses_jsonschema import JsonSchemaMixin, SchemaType

from .data_types import JsonDict


def load_api_spec(
    path: Union[Path, str], version: str, components: Optional[List[JsonSchemaMixin]] = None
) -> Tuple[JsonDict, Dict[str, List[str]]]:
    """Loads the API spec YAML and adds the schema definitions"""
    with open(path, "r") as spec_file:
        spec = yaml.safe_load(spec_file)
        for component in components or []:
            spec["components"]["schemas"].update(component.all_json_schemas(schema_type=SchemaType.SWAGGER_V3))
        spec["info"]["version"] = version
        global_params = spec["components"].get("parameters", [])
        operation_parameters = {}
        for path_data in spec["paths"].values():
            for operation_data in path_data.values():
                param_names = []
                if "parameters" in operation_data:
                    for param in operation_data["parameters"]:
                        if "$ref" in param:
                            param_names.append(global_params[param["$ref"].split("/")[-1]]["name"])
                        else:
                            param_names.append(param["name"])
                operation_parameters[operation_data["operationId"]] = param_names
        return spec, operation_parameters


class AppResolver(Resolver):
    """Override `Resolver` to prefix operationId with the module name.

    **Note:** This can be done with the `x-swagger-router-controller` property but it
    doesn't seem like this can be set globally for the whole api.
    """

    def resolve_operation_id(self, operation):
        parent = ".".join(__name__.split(".")[:-1])
        operation_id = parent + ".api." + super().resolve_operation_id(operation)
        function = self.resolve_function_from_operation_id(operation_id)
        # Check that all of the parameter names match
        arguments = signature(function).parameters
        if "kwargs" in arguments:
            return operation_id
        for parameter in operation._operation.get("parameters", []):
            assert parameter["name"] in arguments, f"{parameter['name']} not in {function.__name__} arguments"
        return operation_id


def _mk_response(content: Any, status: int):
    return ConnexionResponse(body=content, status_code=status)
