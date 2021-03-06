import json

import pytest

from sauron.models import RuleModel


@pytest.fixture
def json_data():
    return """
    {
        "conditions": [
            {
                "name": "condition_1",
                "args": {
                    "int1": 1,
                    "int2": 3
                }
            }
        ],
        "actions": [
            {
                "name": "action_1",
                "args": {
                    "int_list": [1,2,3],
                    "my_string": "teste"
                }
            }
        ]
    }
    """


def test_can_deserialize_json_conditions(json_data):
    rule_dict = json.loads(json_data)
    rule = RuleModel(**rule_dict)
    assert len(rule.conditions) == 1
    assert rule.conditions[0].name == "condition_1"
    assert rule.conditions[0].args == {"int1": 1, "int2": 3}


def test_can_deserialize_json_actions(json_data):
    rule_dict = json.loads(json_data)
    rule = RuleModel(**rule_dict)
    assert len(rule.actions) == 1
    assert rule.actions[0].name == "action_1"
    assert rule.actions[0].args == {
        "int_list": [1, 2, 3],
        "my_string": "teste",
    }
