from sauron.rule_engine import RuleEngine
from enum import Enum


engine = RuleEngine()


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
