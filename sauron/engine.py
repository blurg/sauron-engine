from typing import List, Dict, Callable, Union, Any, cast
from .models import JobModel
import json as json
import inspect
from collections import OrderedDict
from enum import Enum

from .parsers import DefaultParser


class Engine:
    job_model_class = JobModel

    parser_class = DefaultParser
    parsed_jobs: List[JobModel] = []

    callables_collected = OrderedDict()

    def __init__(self, job_model=None, parser_class=None):
        """
        Constructor that allows to customize:
        - job model
        - parser class: responsilbe to parse jobs
        """

        if job_model:
            self.job_model_class = job_model

        if parser_class:
            self.parser_class = parser_class


    def __add_callable(self, function, verbose_name):
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

        def decorator(function):
            verbose_name = kwargs.get("verbose_name", None)
            if args:
                verbose_name = args[0]
            self.__add_callable(function, verbose_name)
            return function

        return decorator

    def apply_job_call(self, func_name, session):
        target_func = self.callables_collected[func_name]["function"]
        job_args = [
            job.args for job in self.parsed_jobs.jobs if job.name == func_name
        ]
        if job_args:
            job_args = job_args[0]
        else:
            raise ValueError(f'No job added with function name: {func_name}')

        if job_args:
            func_result = target_func(session=session, **job_args)
        else:
            func_result = target_func(session=session)

        # append result of function called into sessino
        session[func_name] = {"return": func_result}


    def parse(self, unparsed_jobs):
        p = self.parser_class()
        parsed_jobs = p.parse(unparsed_jobs)
        self.parsed_jobs = parsed_jobs

    def run(self, jobs, session):
        """
        Code that executes each Job respecting the jobs sequence
        """
        self.parse(jobs)
        for job in self.parsed_jobs.jobs:
            self.apply_job_call(job.name, session)
