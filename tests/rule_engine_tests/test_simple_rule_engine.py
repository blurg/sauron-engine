import inspect

import pytest

from sauron_rule_engine import __version__
from sauron_rule_engine.rule_engine import RuleEngine


@pytest.fixture
def json_rule_can_increment():
    return """
    {
        "conditions": [
            {
                "name": "is_smaller_than",
                "args": {
                    "compared_to": 2
                }
            }
        ],
        "actions": [
            {
                "name": "increment_number"
            }
        ]
    }
    """


def test_can_subclass_and_instantiate_rule_engine():
    class ConcreteRuleProcessor(RuleEngine):
        ...

    instance = ConcreteRuleProcessor()
    parents = inspect.getmro(instance.__class__)
    assert parents[1] == RuleEngine


def test_can_add_condition_to_engine():
    engine = RuleEngine()

    @engine.condition()
    def is_equal(a: int, b: int) -> bool:
        return a == b

    assert len(engine.conditions) == 1
    assert engine.conditions["is_equal"]["function"](1, 1)
    assert not engine.conditions["is_equal"]["function"](1, 2)


def test_can_add_action_to_engine():
    engine = RuleEngine()

    @engine.action()
    def is_equal(a: int, b: int) -> bool:
        return a == b

    assert len(engine.actions) == 1
    assert hasattr(engine.actions["is_equal"]["function"], "__call__")
    assert engine.actions["is_equal"]["function"](1, 1)
    assert not engine.actions["is_equal"]["function"](1, 2)


def test_can_run_rules(json_rule_can_increment):
    engine = RuleEngine()
    number_to_be_incremented = 1

    @engine.condition()
    def is_smaller_than(compared_to: int) -> bool:
        return number_to_be_incremented < compared_to

    @engine.action()
    def increment_number() -> None:
        nonlocal number_to_be_incremented
        number_to_be_incremented += 1

    engine.run(json_rule_can_increment)
    assert number_to_be_incremented == 2


def test_can_run_rules_and_will_respect_them(json_rule_can_increment):
    engine = RuleEngine()
    number_to_be_incremented = 1

    @engine.condition()
    def is_smaller_than(compared_to: int) -> bool:
        return number_to_be_incremented < compared_to

    @engine.action()
    def increment_number() -> None:
        nonlocal number_to_be_incremented
        number_to_be_incremented += 1

    engine.run(json_rule_can_increment)
    engine.run(json_rule_can_increment)
    engine.run(json_rule_can_increment)
    assert number_to_be_incremented == 2


def test_version():
    assert __version__ == "0.1.1"
