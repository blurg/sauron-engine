from collections import OrderedDict
from typing import List, Dict, Callable, Union, Any, Type
from .models import JobModel
from enum import Enum
import inspect
import json as json_lib
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO


class MyYAML(YAML):
    """
        ruamel.yaml lib was chosen as it supports yaml1.2, this gives us json parsing
        together with yaml parsing
        Allows to dump yaml to a string. This can/should be reviewed as this is less
        performatic than writing to a file or stdout according to docs
        https://yaml.readthedocs.io/en/latest/example.html#output-of-dump-as-a-string
    """

    def dump(self, data, stream=None, **kw):
        inefficient = False
        if stream is None:
            inefficient = True
            stream = StringIO()
        YAML.dump(self, data, stream, **kw)
        if inefficient:
            return stream.getvalue()


class DefaultExporter:
    def __init__(self):
        self.yaml: Type[YAML] = MyYAML(typ="safe")

    def get_job_types(self):
        # TODO: implement this method to get the job types available
        ...

    @staticmethod
    def get_param_info(param):
        """
        Get Type and Defaults of the parameter. If the parameter is an Enum,
        also gets the choices available
        """
        annotation = param.annotation
        name = annotation.__name__
        choices = None
        if Enum in annotation.__mro__:
            choices = [choice for choice in annotation.__members__]
        defaults = param.default
        if defaults is param.empty:
            defaults = None
        return name, choices, defaults

    @classmethod
    def _get_function_metadata(
        cls, input_function: Callable
    ) -> Dict[str, Any]:
        """
            Metadata about arguments documentation and the function itself
        """
        signature: inspect.Signature = inspect.signature(input_function)
        arguments_metadata: Dict[str, Dict[str, Any]] = {}
        for key, parameter in signature.parameters.items():
            arg_type, arg_choices, arg_defaults = cls.get_param_info(parameter)
            arguments_metadata[key] = {
                "default": arg_defaults,
                "type": arg_type,
                "choices": arg_choices,
            }

        metadata = {
            "args": arguments_metadata,
            "doc": inspect.getdoc(input_function),
            "name": input_function.__name__,
        }

        return metadata

    def get_metadata(self, input_function: Dict[str, Any]) -> Dict[str, Any]:
        metadata = self._get_function_metadata(input_function["function"])
        verbose_name = input_function.get("verbose_name", None)
        if verbose_name:
            metadata["name"] = verbose_name
        metadata["type"] = input_function.get("type", "job")

        return metadata

    def export_job(self, jobs: Dict[str, Any]) -> Dict[str, Any]:
        result = {}
        for name, item in jobs.items():
            result[name] = self.get_metadata(item)
        return result

    def export_jobs(
        self, data: Dict[str, Callable], fmt: str = "dict"
    ) -> Union[str, Dict[str, Any]]:
        jobs = self.export_job(data)
        if fmt == "json":
            return json_lib.dumps(jobs)
        elif fmt == "yaml":
            return self.yaml.dump(jobs)
        else:
            return jobs


class RuleEngineExporter(DefaultExporter):
    def __init__(self):
        self.yaml: Type[YAML] = MyYAML(typ="safe")

    def export_job(self, jobs: Dict[str, Any]) -> Dict[str, Any]:
        result = super().export_job(jobs)
        # Separar jobs por tipo
        result_splited_by_type = {}
        for key, value in result.items():
            current_type = result_splited_by_type.get(value["type"], {})
            current_type[key] = value
            result_splited_by_type[value["type"]] = current_type
        print(result_splited_by_type)
        return result_splited_by_type

    def export_jobs(
        self, data: Dict[str, Callable], fmt: str = "dict"
    ) -> Union[str, Dict[str, Any]]:
        jobs = self.export_job(data)
        if fmt == "json":
            return json_lib.dumps(jobs)
        elif fmt == "yaml":
            return self.yaml.dump(jobs)
        else:
            return jobs
