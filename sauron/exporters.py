from collections import OrderedDict
from typing import List, Dict, Callable, Union, Any, Type
from .models import JobModel
from enum import Enum
import inspect
import json as json_lib


class DefaultExporter:
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
    def __get_function_metadata(
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
        metadata = self.__get_function_metadata(input_function["function"])
        verbose_name = input_function.get("verbose_name", None)
        if verbose_name:
            metadata["name"] = verbose_name

        return metadata

    def export_job(self, jobs: Dict[str, Any]) -> Dict[str, Any]:
        result = {}
        for name, item in jobs.items():
            result[name] = self.get_metadata(item)
        return result

    def export_jobs(
        self, data: Dict[str, Callable], json: bool = False
    ) -> Union[str, Dict[str, Any]]:
        jobs = self.export_job(data)
        if json:
            return json_lib.dumps(jobs)
        else:
            return jobs
