import pytest
from sauron_rule_engine.rule_engine import RuleEngine
from enum import Enum

engine = RuleEngine()


class Color(str, Enum):
    red = "R"
    green = "G"
    blue = "B"


@engine.condition("Primeira Condição")
def first_condition(lower_number: int = 10, greater_number: int = 20) -> bool:
    """
    Checks if first number is lower than the first
    - lower_number: Number expected to be low
    - higher_number: Number expected to be high
    """
    return lower_number < greater_number


@engine.condition("é vermelho?")
def is_red(color: Color) -> bool:
    """
    Checks if the color is red
    """
    return color == color.red


@engine.condition()
def condition_without_default(number: int) -> bool:
    """
    Checks if number is greater than 10
    """
    return number > 10


@engine.condition()
def second_condition_true():
    return True


@engine.condition()
def condition_false():
    return False


@engine.condition()
def condition_failure():
    raise Exception


@engine.action()
def action_success():
    print("success")


@engine.action("Ação Óbvia")
def obvious_action(lower_number: int = 10, greater_number: int = 20) -> None:
    """
    Prints a statement Asserting that the first number is lower than the second number
    - lower_number: Number expected to be low
    - higher_number: Number expected to be high
    """
    print(f"{lower_number} < {greater_number}")


# CONDITIONS


def test_get_funtion_metadata_docstring():
    conditions = engine.export_conditions()
    assert (
        conditions["first_condition"]["doc"]
        == "Checks if first number is lower than the first\n- lower_number: Number expected to be low\n- higher_number: Number expected to be high"
    )


def test_get_funtion_metadata_can_get_first_arg_type():
    conditions = engine.export_conditions()

    assert (
        conditions["first_condition"]["args"]["lower_number"]["type"] == "int"
    )


def test_can_generate_conditions_dictionary_and_default_value_of_argument_lower_number_is_right():
    conditions = engine.export_conditions()

    assert (
        conditions["first_condition"]["args"]["lower_number"]["default"] == 10
    )


def test_can_generate_conditions_dictionary_and_verbose_name():
    conditions = engine.export_conditions()

    assert conditions["first_condition"]["name"] == "Primeira Condição"


def test_can_generate_conditions_dictionary_and_function_name():
    conditions = engine.export_conditions()

    assert (
        conditions["second_condition_true"]["name"] == "second_condition_true"
    )


# ACTIONS


def test_can_generate_actions_dictionary_and_function_name_with_verbose_name():
    actions = engine.export_actions()
    print(actions)

    assert actions["obvious_action"]["name"] == "Ação Óbvia"


def test_can_generate_actions_dictionary_and_function_name():
    actions = engine.export_actions()
    print(actions)

    assert actions["action_success"]["name"] == "action_success"


def test_get_action_metadata_docstring():
    actions = engine.export_actions()
    assert (
        actions["obvious_action"]["doc"]
        == "Prints a statement Asserting that the first number is lower than the second number\n- lower_number: Number expected to be low\n- higher_number: Number expected to be high"
    )


def test_get_action_metadata_can_get_first_arg_type():
    actions = engine.export_actions()

    assert actions["obvious_action"]["args"]["lower_number"]["type"] == "int"


def test_can_generate_actions_dictionary_and_default_value_of_argument_lower_number_is_right():
    actions = engine.export_actions()

    assert actions["obvious_action"]["args"]["lower_number"]["default"] == 10


def test_can_generate_metadata_dictionary_and_default_value_of_argument_lower_number_is_right_for_action():
    metadata = engine.export_metadata()

    assert (
        metadata["actions"]["obvious_action"]["args"]["lower_number"][
            "default"
        ]
        == 10
    )


def test_can_generate_metadata_json_and_default_value_of_argument_lower_number_is_right_for_action():
    metadata = engine.export_metadata(json=True)

    assert type(metadata) == str


def test_can_handle_enum_types_on_condition():
    conditions = engine.export_conditions()
    assert conditions["is_red"]["args"]["color"]["choices"] == [
        "red",
        "green",
        "blue",
    ]
