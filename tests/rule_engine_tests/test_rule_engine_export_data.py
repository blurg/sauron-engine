from enum import Enum

from sauron.rule_engine import RuleEngine

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


def test_can_generate_metadata_json_and_default_value_of_argument_lower_number_is_right_for_action():
    metadata = engine.export_metadata(fmt="json")
    assert isinstance(metadata, str)


def test_can_handle_enum_types_on_condition():
    jobs = engine.export_metadata()
    print(jobs["condition"])
    assert jobs["condition"]["is_red"]["args"]["color"]["choices"] == [
        "red",
        "green",
        "blue",
    ]
