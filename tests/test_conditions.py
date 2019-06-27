import pytest
from sauron_rule_engine.rule_engine import RuleEngine


engine = RuleEngine()


@engine.condition
def condition_true():
    return True


@engine.condition
def second_condition_true():
    return True


@engine.condition
def condition_false():
    return False


@engine.condition
def condition_failure():
    raise Exception


@engine.action
def action_success():
    print("success")


def test_doesnt_execute_on_condition_false(capsys):
    rule = """
    {
        "conditions": [
            {
                "name": "condition_false",
                "arguments": {
                }
            }
        ],
        "actions": [
            {
                "name": "action_success"
            }
        ]
    }
    """

    engine.run(rule)
    captured = capsys.readouterr()
    assert captured.out == ""


def test_executes_on_condition_true(capsys):
    rule = """
    {
        "conditions": [
            {
                "name": "condition_true",
                "arguments": {
                }
            }
        ],
        "actions": [
            {
                "name": "action_success"
            }
        ]
    }
    """

    engine.run(rule)
    captured = capsys.readouterr()
    assert captured.out == "success\n"


def test_crashes_on_condition_crash(capsys):
    rule = """
    {
        "conditions": [
            {
                "name": "condition_failure",
                "arguments": {
                }
            }
        ],
        "actions": [
            {
                "name": "action_success"
            }
        ]
    }
    """
    with pytest.raises(Exception):
        assert engine.run(rule)
