import pytest
from sauron_rule_engine.rule_engine import RuleEngine


engine = RuleEngine()


@engine.condition
def first_condition(lower_number: int = 10, greater_number: int = 20) -> bool:
    """
    Checks if first number is lower than the first
    - lower_number: Number expected to be low
    - higher_number: Number expected to be high
    """
    return lower_number < greater_number


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


def test_get_funtion_metadata_can_args_data():
    function = first_condition()
    result = engine.get_function_metadata(function)
    assert result.get("args", None) is not None


def test_get_funtion_metadata_docstring():
    function = first_condition()
    result = engine.get_function_metadata(function)
    assert (
        result["doc"]
        == "Checks if first number is lower than the first\n- lower_number: Number expected to be low\n- higher_number: Number expected to be high"
    )


def test_get_funtion_metadata_can_get_first_arg_type():
    function = first_condition()
    result = engine.get_function_metadata(function)
    print(result["args"])
    assert result["args"]["lower_number"]["type"] == "int"


def test_get_funtion_metadata_can_get_first_default():
    function = first_condition()
    result = engine.get_function_metadata(function)
    assert result["args"]["lower_number"]["default"] == 10


def test_can_generate_conditions_dictionary():
    conditions = engine.export_conditions()

    assert type(conditions) == dict


def test_can_generate_conditions_dictionary_and_default_value_of_argument_lower_number_is_right():
    conditions = engine.export_conditions()

    assert (
        conditions["first_condition"]["args"]["lower_number"]["default"] == 10
    )


# def test_dictionary_contains_type_data_about_first_condition():
#     conditions = engine.export_conditions()
#     condition = conditions["first_condition"]
#     input_types = condition.get("input_types", None)
#     assert input_types is not None


# def test_dictionary_contains_type_data_about_first_condition_and_lower_number_is_int():
#     conditions = engine.export_conditions()
#     condition = conditions["first_condition"]
#     input_types = condition.get("input_types", None)
#     assert input_types["lower_number"] == "Int"
