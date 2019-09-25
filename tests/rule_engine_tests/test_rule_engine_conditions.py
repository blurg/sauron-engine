import pytest

from sauron.rule_engine import RuleEngine

engine = RuleEngine()


@engine.condition()
def condition_true(session):
    return True


@engine.condition()
def second_condition_true(session):
    return True


@engine.condition()
def condition_false(session):
    return False


@engine.condition()
def condition_failure(session):
    raise Exception


@engine.action()
def action_success(session):
    print("success")


def test_doesnt_execute_on_condition_false(capsys):
    rule = """
    {
        "conditions": [
            {
                "name": "condition_false",
                "args": {
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
                "args": {
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
                "args": {
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
