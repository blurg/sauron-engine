from typing import List, Dict, Callable, Union
from .models import RuleModel, ConditionModel, ActionModel
import json


class RuleEngine:
    def __init__(self, *args, **kwargs):
        self.conditions: Dict[str, Callable] = {}
        self.actions: Dict[str, Callable] = {}
        return super().__init__(*args, **kwargs)

    def __add_condition(self, function: Callable) -> None:
        self.conditions[function.__name__] = function

    def __add_action(self, function: Callable) -> None:
        self.actions[function.__name__] = function

    def condition(self, function: Callable) -> Callable:
        """
        Decorator so rules can be called as follows:
        @obj.condition
        def my_function():
            return None
        """

        def decorator() -> Callable:
            return function

        self.__add_condition(function)
        return decorator

    def action(self, function: Callable) -> Callable:
        """
        Decorator so actions can be called as follows:
        @obj.action
        def my_function():
            return None
        """

        def decorator() -> Callable:
            return function

        self.__add_action(function)
        return decorator

    def parse_rule(self, rule: Union[dict, str]) -> RuleModel:
        """
        Rules are received either as json or as dict, parse and return pydantic model
        """
        if type(rule) == str:
            rule: dict = json.loads(rule)
        return RuleModel(**rule)

    def __apply_conditions(self, conditions: List[ConditionModel]) -> bool:
        """
            Auxiliary function to apply rules, currently the only option is to run
            on AND mode, that means that any False condition will result in False

        """
        should_continue: bool = True
        for condition in conditions:
            if condition.arguments:
                should_continue &= self.conditions[condition.name](
                    **condition.arguments
                )
            else:
                should_continue &= self.conditions[condition.name]()

        return should_continue

    def __run_actions(self, actions: List[ConditionModel]) -> bool:
        """
            Actions are applied sequentially
        """
        for action in actions:
            if action.arguments:
                self.actions[action.name](**action.arguments)
            else:
                self.actions[action.name]()
        return True

    def run(self, rule: Union[dict, str]) -> bool:
        """
            Run rule engine:
            - rule - Json string or dict on the right format containing
            a rule, it specifies which conditions should be checked and
            which actions should be executed if conditions are met
        """
        rule: RuleModel = self.parse_rule(rule)
        should_continue: bool = self.__apply_conditions(rule.conditions)

        if should_continue:
            self.__run_actions(rule.actions)
            return True
        return False

