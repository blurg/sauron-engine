from typing import Callable, Optional, Type

from .engine import Engine
from .exporters import DefaultExporter, RuleEngineExporter
from .parsers import DefaultParser, RuleEngineParser


class RuleEngine(Engine):
    parser_class: Type[DefaultParser] = RuleEngineParser
    exporter_class: Type[DefaultExporter] = RuleEngineExporter

    def condition(self, *args, **kwargs):
        def decorator(function: Callable):
            verbose_name: Optional[str] = kwargs.get("verbose_name", None)
            if args:
                verbose_name = args[0]
            if verbose_name is None:
                verbose_name = function.__name__
            self._add_callable(function, verbose_name, job_type="condition")
            return function

        return decorator

    def action(self, *args, **kwargs):
        def decorator(function: Callable):
            verbose_name: Optional[str] = kwargs.get("verbose_name", None)
            if args:
                verbose_name = args[0]
            if verbose_name is None:
                verbose_name = function.__name__
            self._add_callable(function, verbose_name, job_type="action")
            return function

        return decorator
