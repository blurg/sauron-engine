from typing import List, Dict, Callable, Union, Any, cast, Type
from .models import JobModel
import json as json
import inspect
from collections import OrderedDict
from enum import Enum

from .parsers import DefaultParser


class Engine:

    job_model_class: Type[JobModel] = JobModel
    parser_class: Type[DefaultParser] = DefaultParser

    parsed_rule: List[Type[JobModel]] = []

    session: Dict[str, Any] = {}
    callables_collected: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()

    def __init__(
        self,
        context: Dict[str, Any] = None,
        job_model: Type[JobModel] = None,
        parser_class: Type[DefaultParser] = None,
    ):
        """
        - Sessions can be initialized with a context provided by the user
        - Job Model and Parser can be changed
        """
        if context:
            self.session = context

        if job_model:
            self.job_model_class = job_model

        if parser_class:
            self.parser_class = parser_class

    def __add_callable(self, function: Callable, verbose_name: str):
        self.callables_collected[function.__name__] = {
            "function": function,
            "verbose_name": verbose_name,
        }

    def job(self, *args, **kwargs):
        """
        Decorator so jobs can be called as follows:
        @obj.job
        def my_function():
            return None
        """

        def decorator(function: Callable):
            verbose_name: str = kwargs.get("verbose_name", None)
            if args:
                verbose_name = args[0]
            self.__add_callable(function, verbose_name)
            return function

        return decorator

    def before_job_call_hook(self):
        ...

    def after_job_call_hook(self):
        ...

    def apply_job_call(self, func_name: str, session: Dict[str, Any]):
        target_func = self.callables_collected.get(func_name).get("function")
        rules: List[Any] = []

        for rule in self.parsed_rule:
            if rule.name == func_name:
                rules.append(rule)

        if rules[0]:
            job: Type[JobModel] = rules[0]
        else:
            raise ValueError(f"No job added with function name: {func_name}")

        if job.args:
            func_result = target_func(session=session, **job.args)
        else:
            func_result = target_func(session=session)

        # append result of function called into sessino
        session[func_name] = {"return": func_result}

    def parse(self, unparsed_rule: Union[str, Dict[str, Any]]):
        """
            Parses rules
        """
        p = self.parser_class()
        parsed_rule = p.parse(unparsed_rule)
        print("parsed_rule")
        self.parsed_rule = parsed_rule
        return parsed_rule

    def run(
        self, rule: Union[str, Dict[str, Any]], session: Dict[str, Any] = None
    ):
        """
        Executes each job passing the current session to them
        """

        if session:
            session = session
        else:
            session = self.session

        for job in self.parse(rule):
            print(job)
            self.apply_job_call(job.name, session)
