from enum import Enum

import yaml

from sauron.rule_engine import RuleEngine

engine = RuleEngine()


@engine.condition("First Condition")
def first_condition(lower_number: int = 10, greater_number: int = 20) -> bool:
    return lower_number < greater_number


@engine.condition("Second Condition")
def second_condition():
    return True


class Color(str, Enum):
    red = "R"
    green = "G"
    blue = "B"


@engine.condition("Choice Condition")
def choice_condition(color: Color) -> bool:
    return color == color.red


@engine.action("First Action")
def first_action(lower_number: int = 10, greater_number: int = 20):
    print(f"{lower_number} < {greater_number}")


@engine.action("Second Action")
def second_action():
    return True


class TestExportYaml:
    def setup(self):
        self.export_yaml = engine.export_metadata(fmt="yaml")
        self.export = engine.export_metadata()

    def test_export_is_a_valid_yaml(self):
        print(self.export_yaml)
        assert yaml.safe_load(self.export_yaml)

    def test_export_has_all_conditions(self):
        conditions = self.export["condition"]
        assert len(conditions) == 3
        assert "first_condition" and "second_condition" in conditions

    def test_export_first_condition_args_(self):
        conditions_args = self.export["condition"]["first_condition"]["args"]
        assert len(conditions_args) == 2
        assert "lower_number" and "greater_number" in conditions_args

    def test_export_second_condition_args(self):
        conditions_args = self.export["condition"]["second_condition"]["args"]
        assert len(conditions_args) == 0

    def test_export_choice_condition_args(self):
        conditions_args = self.export["condition"]["choice_condition"]["args"]
        assert len(conditions_args) == 1

    def test_export_first_condition_args_content(self):
        condition = self.export["condition"]["first_condition"]["args"]
        assert "lower_number" in condition
        assert "greater_number" in condition
        assert condition["lower_number"]["default"] == 10
        assert condition["greater_number"]["default"] == 20
        assert condition["greater_number"]["type"] == "int"
        assert condition["greater_number"]["choices"] is None

    def test_export_second_condition_args_content(self):
        condition = self.export["condition"]["second_condition"]["args"]
        assert condition == {}

    def test_export_third_condition_args_content(self):
        condition = self.export["condition"]["choice_condition"]["args"]
        assert "color" in condition
        assert len(condition["color"]["choices"]) == 3
        assert condition["color"]["choices"] == ["red", "green", "blue"]
        assert condition["color"]["type"] == "Color"

    def test_checking_condition_type(self):
        first_condition = self.export["condition"]["first_condition"]["type"]
        second_condition = self.export["condition"]["second_condition"]["type"]
        choice_condition = self.export["condition"]["choice_condition"]["type"]
        assert first_condition == "condition"
        assert second_condition == "condition"
        assert choice_condition == "condition"

    def test_export_has_all_actions(self):
        actions = self.export["action"]
        assert len(actions) == 2
        assert "first_action" and "second_action" in actions

    def test_export_first_action_args(self):
        action_args = self.export["action"]["first_action"]["args"]
        assert len(action_args) == 2
        assert "lower_number" and "greater_number" in action_args

    def test_export_second_action_args(self):
        action_args = self.export["action"]["second_action"]["args"]
        assert len(action_args) == 0

    def test_checking_action_type(self):
        first_action = self.export["action"]["first_action"]["type"]
        second_action = self.export["action"]["second_action"]["type"]
        assert first_action == "action"
        assert second_action == "action"
