<h1 align="center">Sauron Rule engine - One engine to rule them all </h1>
<p>
  <img src="https://img.shields.io/badge/version-0.1-blue.svg?cacheSeconds=2592000" />
  <a href="https://twitter.com/joaovoce">
    <img alt="Twitter: joaovoce" src="https://img.shields.io/twitter/follow/joaovoce.svg?style=social" target="_blank" />
  </a>
</p>

> A simple rule engine to be used in python, it is based on simple rules and actions that can be chained with each other. The idea is to run the rule processor on events and have it mutate data or trigger actions

Heavily inspired on FastAPI

## Install

```sh
pip install sauron-rule-engine
```

## Use it

A simple example of the usage

```python
from sauron_rule_engine.rule_engine import RuleEngine

#instantiate your engine
engine = RuleEngine()

#just a dumb variable so we can see the actions in use
number_to_be_incremented = 1

@engine.condition
def is_smaller_than(compared_to: int) -> bool:
    return number_to_be_incremented < compared_to

@engine.action
def increment_number() -> None:
    nonlocal number_to_be_incremented
    number_to_be_incremented += 1

# Then just use your engine
if __name__ == "__main__":
  print(number_to_be_incremented)
  ## 1

  engine.run(json_rule_can_increment)
  print(number_to_be_incremented)
  ## 2

  engine.run(json_rule_can_increment)
  print(number_to_be_incremented)
  ## 2

```

## Features coming to town

- Exporting a json string with the conditions and actions in a given engine
- Exported conditions and actions should include sane typing and docstring exposure
- Support pydantic types
- Support for choices fields with enum
- Support for complex types with hints to the frontend (like a range for an int type

## Author

👤 **João Ricardo Lhullier Lugão**

- Twitter: [@joaovoce](https://twitter.com/joaovoce)
- Github: [@jlugao](https://github.com/jlugao)

## Show your support

Give a ⭐️ if this project helped you!

---

_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
