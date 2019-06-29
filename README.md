<h1 align="center">Sauron Rule engine - One engine to rule them all </h1>
<p>
  <img src="https://img.shields.io/badge/version-0.1-blue.svg?cacheSeconds=2592000" />
  <img src="https://circleci.com/gh/jlugao/sauron-rule-engine/tree/master.svg?style=svg" />
  <a href='https://coveralls.io/github/jlugao/sauron-rule-engine?branch=master'><img src='https://coveralls.io/repos/github/jlugao/sauron-rule-engine/badge.svg?branch=master&service=github' alt='Coverage Status' /></a>

<img alt="GitHub" src="https://img.shields.io/github/license/jlugao/sauron-rule-engine.svg?style=plastic">
  <a href="https://twitter.com/joaovoce">
    <img alt="Twitter: joaovoce" src="https://img.shields.io/twitter/follow/joaovoce.svg?style=social" target="_blank" />
  </a>
</p>

> A simple rule engine to be used in python, it is based on simple rules and actions that can be chained with each other. The idea is to run the rule processor on events and have it mutate data or trigger actions

Heavily inspired on FastAPI. We use type annotations in our engine so that we can export data to other systems or frontends to convey what conditions and actions are possible using that engine

## Install

```sh
pip install sauron-rule-engine
```

## Concepts

Sauron rule engine is based on custom functions that can be called by a rule.

### Condition

Condition to be satisfied in order for the actions to run, they can take some or no parameters at all
Multiple conditions can be chained in order to create more complex ones, currently all chained conditions must be satisfied

### Action

An Action is the intented result. Usually they are there to mutate state or trigger/schedule other kinds of actions in your system. Actions can also be chained and will run in order.

### Rule

A Rule is a dict or json string containing the conditions and actions and the arguments they should be run with. Usually those rules will be built by a frontend to match complex and adaptable business rules from your customer

## Use it

A simple example of the usage

```python
from sauron_rule_engine.rule_engine import RuleEngine

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
from sauron_rule_engine.rule_engine import RuleEngine
from enum import Enum

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

```

## Export Conditions and Actions

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

## More Features coming to town

- Support pydantic types
- Support for complex types with hints to the frontend (like a range for an int type

## Author

👤 **João Ricardo Lhullier Lugão**

- Twitter: [@joaovoce](https://twitter.com/joaovoce)
- Github: [@jlugao](https://github.com/jlugao)

## Show your support

Give a ⭐️ if this project helped you!

---

_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
