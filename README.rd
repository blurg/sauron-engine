#Sauron Rule engine - One engine to rule them all

> A simple rule engine to be used in python, it is based on simple rules and actions that can be chained with each other. The idea is to run the rule processor on events and have it mutate data or trigger actions

## Install

```sh
pip install sauron-rule-engine
```

## Use it

A simple example of the usage

```python
from sauron_rule_engine.rule_engine import GenericRuleProcessor

class CounterRuleProcessor(GenericRuleProcessor):

    # CONDITIONS
    @staticmethod
    def counter_lt(value):
        return counter < value

    # ACTIONS
    @staticmethod
    def increment_counter():
        global counter
        counter += 2


counter = 0

input_rule1 = {
    "when": "event 1",
    "condition": "counter_lt",
    "value": 1,
    "action": "increment_counter",
}

if __name__ == "__main__":
    print(f"counter value: {counter}")
    processor = CounterRuleProcessor()
    processor.run(input_rule1)
    print(f"counter value: {counter}")
    processor.run(input_rule1)
    print(f"counter value: {counter}")
```

## Author

👤 **João Ricardo Lhullier Lugão**

- Twitter: [@joaovoce](https://twitter.com/joaovoce)
- Github: [@jlugao](https://github.com/jlugao)

## Show your support

Give a ⭐️ if this project helped you!

---

_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
