from typing import Union
from decimal import Decimal


def always_true(context):
    """
    This method is a sample method to return True always
    """
    return True


def times_two(context, input: Union[float, int, Decimal]):
    """
    This method is a sample method to return True always
    """
    return input * 2
