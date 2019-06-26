from sauron_rule_engine import __version__
from sauron_rule_engine.rule_engine import GenericRuleProcessor
import pytest
import inspect


def test_can_subclass_and_instantiate_rule_engine():
    class ConcreteRuleProcessor(GenericRuleProcessor):
        ...

    instance = ConcreteRuleProcessor()
    parents = inspect.getmro(instance.__class__)
    assert parents[1] == GenericRuleProcessor


def test_version():
    assert __version__ == "0.1.1"

