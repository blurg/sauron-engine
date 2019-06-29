from typing import List, Dict, Callable, Union, Any, cast
from .models import RuleModel, ConditionModel, ActionModel
import json
import inspect
import json as json_lib
from enum import Enum


class RuleEngine:
    def __init__(self, *args, **kwargs):
        self.conditions: Dict[str, Callable] = {}
        self.actions: Dict[str, Callable] = {}
        self.metadata: Dict[str, Callable] = {}
        return super().__init__(*args, **kwargs)

    @staticmethod
    def get_param_info(param):
        """
        Get Type, Choices and Defaults of the parameter
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

    def __add_condition(
        self, function: Callable, verbose_name: str = None
    ) -> None:
        self.conditions[function.__name__] = {
            "function": function,
            "verbose_name": verbose_name,
        }

    def __add_action(
        self, function: Callable, verbose_name: str = None
    ) -> None:
        self.actions[function.__name__] = {
            "function": function,
            "verbose_name": verbose_name,
        }

    def condition(self, *args, **kwargs) -> Callable:
        """
        Decorator so rules can be called as follows:
        @obj.condition
        def my_function():
            return None
        """

        def decorator(function) -> Callable:
            verbose_name = kwargs.get("verbose_name", None)
            if args:
                verbose_name = args[0]
            self.__add_condition(function, verbose_name)
            return function

        return decorator

    def action(self, *args, **kwargs) -> Callable:
        """
        Decorator so actions can be called as follows:
        @obj.action
        def my_function():
            return None
        """

        def decorator(function) -> Callable:
            verbose_name = kwargs.get("verbose_name", None)
            if args:
                verbose_name = args[0]
            self.__add_action(function, verbose_name)
            return function

        return decorator

    def parse_rule(
        self, untreated_rule: Union[Dict[Any, Any], str]
    ) -> RuleModel:
        """
        Rules are received either as json or as dict, parse and return pydantic model
        """
        rule: dict = {}
        if type(untreated_rule) == str:
            untreated_rule = cast(str, untreated_rule)
            rule = json.loads(untreated_rule)
        else:
            rule = cast(dict, untreated_rule)
        return RuleModel(**rule)

    def __apply_conditions(self, conditions: List[ConditionModel]) -> bool:
        """
            Auxiliary function to apply rules, currently the only option is to run
            on AND mode, that means that any False condition will result in False

        """
        should_continue: bool = True
        for condition in conditions:
            if condition.arguments:
                should_continue &= self.conditions[condition.name]["function"](
                    **condition.arguments
                )
            else:
                should_continue &= self.conditions[condition.name][
                    "function"
                ]()

        return should_continue

    def __run_actions(self, actions: List[ActionModel]) -> bool:
        """
            Actions are applied sequentially
        """
        for action in actions:
            if action.arguments:
                self.actions[action.name]["function"](**action.arguments)
            else:
                self.actions[action.name]["function"]()
        return True

    def run(self, untreated_rule: Union[Dict[str, Any], str]) -> bool:
        """
            Run rule engine:
            - rule - Json string or dict on the right format containing
            a rule, it specifies which conditions should be checked and
            which actions should be executed if conditions are met
        """
        rule: RuleModel = self.parse_rule(untreated_rule)
        should_continue: bool = self.__apply_conditions(rule.conditions)

        if should_continue:
            self.__run_actions(rule.actions)
            return True
        return False

    def export_generic(self, generic: Dict[str, Any]) -> Dict[str, Any]:
        result = {}
        for name, item in generic.items():
            result[name] = self.get_metadata(item)
        return result

    def export_conditions(self) -> Dict[str, Any]:
        return self.export_generic(self.conditions)

    def export_actions(self) -> Dict[str, Any]:
        return self.export_generic(self.actions)

    def export_metadata(
        self, json: bool = False
    ) -> Union[str, Dict[str, Any]]:
        metadata = {
            "actions": self.export_actions(),
            "conditions": self.export_conditions(),
        }
        if json:
            return json_lib.dumps(metadata)
        else:
            return metadata
