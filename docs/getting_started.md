## A simple usage example

```python
from sauron.rule_engine import RuleEngine

engine = RuleEngine()


@engine.condition("First Condition")
def first_condition(session,lower_number: int = 10, greater_number: int = 20) -> bool:
    """
    Checks if first number is lower than the first
    - lower_number: Number expected to be low
    - higher_number: Number expected to be high
    """
    return lower_number < greater_number


@engine.condition()
def second_condition(session):
    """
    Takes no argument and always returns True
    """
    return True


@engine.action("The Action")
def print_the_equation(
    session, lower_number: int = 10, greater_number: int = 20
) -> None:
    """
    Prints a statement Asserting that the first number is lower than the second number
    - lower_number: Number expected to be low
    - higher_number: Number expected to be high
    """
    print(f"{lower_number} < {greater_number}")


rule = {
    "conditions": [
        {
            "name": "first_condition",
            "args": {"lower_number": 3, "greater_number": 10},
        }
    ],
    "actions": [
        {
            "name": "print_the_equation",
            "args": {"lower_number": 3, "greater_number": 10},
        }
    ],
}


engine.run(rule)
```

## Choices Fields

Choices fields are supported through python's built-in Enum type. Example:

```python
from sauron.rule_engine import RuleEngine
from enum import Enum

class Color(str, Enum):
    red = "R"
    green = "G"
    blue = "B"


@engine.condition("is it red?")
def is_red(session, color: Color) -> bool:
    """
    Checks if the color is red
    """
    return color == color.red

```
