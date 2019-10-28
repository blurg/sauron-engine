You can use the function export_metadata to export your data in a dict or as a json string (just pass `json=True`). Here is an Example and the output:

```python
from sauron_rule_engine.rule_engine import RuleEngine
from enum import Enum

engine = RuleEngine()


@engine.condition("First Condition")
def first_condition(lower_number: int = 10, greater_number: int = 20) -> bool:
    """
    Checks if first number is lower than the first
    - lower_number: Number expected to be low
    - higher_number: Number expected to be high
    """
    return lower_number < greater_number


@engine.condition()
def second_condition():
    """
    Takes no argument and always returns True
    """
    return True


@engine.action("The Action")
def print_the_equation(
    lower_number: int = 10, greater_number: int = 20
) -> None:
    """
    Prints a statement Asserting that the first number is lower than the second number
    - lower_number: Number expected to be low
    - higher_number: Number expected to be high
    """
    print(f"{lower_number} < {greater_number}")


class Color(str, Enum):
    red = "R"
    green = "G"
    blue = "B"


@engine.condition("is it red?")
def is_red(color: Color) -> bool:
    """
    Checks if the color is red
    """
    return color == color.red


metadata = engine.export_metadata(json=True)
print(metadata)

```

Results in the following json to be served to your frontend:

```json
{
  "actions": {
    "print_the_equation": {
      "args": {
        "lower_number": { "default": 10, "type": "int", "choices": null },
        "greater_number": { "default": 20, "type": "int", "choices": null }
      },
      "doc": "Prints a statement Asserting that the first number is lower than the second number\n- lower_number: Number expected to be low\n- higher_number: Number expected to be high",
      "name": "The Action"
    }
  },
  "conditions": {
    "first_condition": {
      "args": {
        "lower_number": { "default": 10, "type": "int", "choices": null },
        "greater_number": { "default": 20, "type": "int", "choices": null }
      },
      "doc": "Checks if first number is lower than the first\n- lower_number: Number expected to be low\n- higher_number: Number expected to be high",
      "name": "First Condition"
    },
    "second_condition": {
      "args": {},
      "doc": "Takes no argument and always returns True",
      "name": "second_condition"
    },
    "is_red": {
      "args": {
        "color": {
          "default": null,
          "type": "Color",
          "choices": ["red", "green", "blue"]
        }
      },
      "doc": "Checks if the color is red",
      "name": "is it red?"
    }
  }
}
```
