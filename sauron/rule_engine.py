from typing import Callable, Type

from .engine import Engine
from .exporters import DefaultExporter, RuleEngineExporter
from .parsers import DefaultParser, RuleEngineParser


class RuleEngine(Engine):
    parser_class: Type[DefaultParser] = RuleEngineParser
    exporter_class: Type[DefaultExporter] = RuleEngineExporter

    def condition(self, *args, **kwargs):
        """
        Decorator so jobs can be called as follows:
        @obj.condition()
        def my_function():
            return None
        """

        def decorator(function: Callable):
            verbose_name: str = kwargs.get("verbose_name", None)
            if args:
                verbose_name = args[0]
            self._add_callable(function, verbose_name, job_type="condition")
            return function

        return decorator

    def action(self, *args, **kwargs):
        """
        Decorator so jobs can be called as follows:
        @obj.action()
        def my_function():
            return None
        """

        def decorator(function: Callable):
            verbose_name: str = kwargs.get("verbose_name", None)
            if args:
                verbose_name = args[0]
            self._add_callable(function, verbose_name, job_type="action")
            return function

        return decorator
