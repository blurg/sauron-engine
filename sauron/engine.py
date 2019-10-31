import time
from collections import OrderedDict
from types import ModuleType
from typing import List, Dict, Callable, Union, Any, Type, Tuple

from blinker import signal
from blinker.base import NamedSignal

from .models import JobModel
from .parsers import DefaultParser
from .exporters import DefaultExporter
import inspect


class Engine:

    job_model_class: Type[JobModel] = JobModel
    parser_class: Type[DefaultParser] = DefaultParser
    exporter_class: Type[DefaultExporter] = DefaultExporter

    parsed_rule: List[JobModel] = []

    session: Dict[str, Any] = {}
    runtime_metrics: Dict[str, Any] = {}

    signals: Dict[str, NamedSignal] = {}

    def __init__(
        self,
        context: Dict[str, Any] = None,
        job_model: Type[JobModel] = None,
        parser_class: Type[DefaultParser] = None,
        exporter_class: Type[DefaultExporter] = None,
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

        if exporter_class:
            self.exporter_class = exporter_class
        self.callables_collected: "OrderedDict[str, Dict[str, Any]]" = OrderedDict()

        self.runtime_metrics["jobs"] = {}
        self.runtime_metrics["total_runtime"] = 0

        self.signals["pre_engine_run"] = signal("pre_engine_run")
        self.signals["post_engine_run"] = signal("post_engine_run")
        self.signals["pre_job_call"] = signal("pre_job_call")
        self.signals["post_job_call"] = signal("post_job_call")

    def _add_callable(
        self, function: Callable, verbose_name: str, job_type: str = "job"
    ):
        self.callables_collected[function.__name__] = {
            "function": function,
            "verbose_name": verbose_name,
            "type": job_type,
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
            self._add_callable(function, verbose_name)
            return function

        return decorator

    def import_jobs(
        self,
        job_module: ModuleType,
        job_metadata: List[Tuple[str, Dict[str, Any]]] = None,
    ):
        if job_metadata is not None:
            raw_job_list: job_metadata
        else:
            try:
                raw_job_list: List[
                    Tuple[str, Dict[str, Any]]
                ] = job_module.jobs_list
            except AttributeError:
                pre_raw_job_list: List[
                    Tuple[str, Callable]
                ] = inspect.getmembers(
                    job_module, predicate=inspect.isfunction
                )
                raw_job_list: List[Tuple[str, Dict[str, Any]]] = [
                    (job[0], {"callable": job[1], "verbose_name": job[0]})
                    for job in pre_raw_job_list
                ]
        for job in raw_job_list:
            self._add_callable(
                job[1].get("callable"),
                verbose_name=job[1].get("verbose_name", job[0]),
                job_type=job[1].get("type", "job"),
            )

    def apply_job_call(
        self, job: JobModel, session: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Any]:
        target_func: Callable = self.callables_collected.get(job.name).get(
            "function"
        )

        pre_signal_payload = {
            "job_name": job.name,
            "job": job,
            "session": session,
        }
        self.signals["pre_job_call"].send(self, **pre_signal_payload)

        if job.args:
            tick_start = time.time()
            result = target_func(session=session, **job.args)
            tick_end = time.time()
        else:
            tick_start = time.time()
            result = target_func(session=session)
            tick_end = time.time()

        self.runtime_metrics["jobs"].setdefault(
            job.name, tick_end - tick_start
        )
        # append result of function called into session
        results = session.get("results", None)
        if not results:
            session["results"] = []
        session["results"].append({"job": job.name, "return": result})
        self.session = session

        post_signal_payload = {
            "job_name": job.name,
            "job": job,
            "session": session,
        }
        self.signals["post_job_call"].send(self, **post_signal_payload)

        return (session, result)

    def parse(self, unparsed_rule: Union[str, Dict[str, Any]]):
        """
            Parses rules
        """
        parser: DefaultParser = self.parser_class()
        parsed_rule: List[JobModel] = parser.parse(unparsed_rule)
        self.parsed_rule = parsed_rule
        return parsed_rule

    def run(
        self, rule: Union[str, Dict[str, Any]], session: Dict[str, Any] = None
    ):
        """
        Executes each job passing the current session to them
        """

        pre_signal_payload = {"rule": rule, "session": session}
        self.signals["pre_engine_run"].send(self, **pre_signal_payload)

        if not session:
            session = self.session

        tick_start = time.time()
        for job in self.parse(rule):
            session, result = self.apply_job_call(job, session)
            if not result:
                break
        tick_end = time.time()

        self.runtime_metrics["total_runtime"] = tick_end - tick_start

        post_signal_payload = {"rule": rule, "session": session}
        self.signals["post_engine_run"].send(self, **post_signal_payload)

    def export_metadata(self, fmt: str = "dict"):
        exporter = self.exporter_class()
        return exporter.export_jobs(self.callables_collected, fmt=fmt)

    def get_signal(self, signal_name):
        if signal_name not in self.signals.keys():
            valid_signal_names = self.signals.keys()
            raise ValueError(
                f"param signal_name: {signal_name} is not valid! Must be one of this: {valid_signal_names}"
            )
        return self.signals[signal_name]
