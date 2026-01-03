from decimal import Decimal
from typing import Any, List, Tuple, Union


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


jobs_list: List[Tuple[str, Any]] = [
    (
        "always_true",
        {
            "verbose_name": "True Always Is",
            "callable": always_true,
            "job_type": "job",
        },
    ),
    (
        "times_two",
        {
            "verbose_name": "Double that",
            "callable": times_two,
            "job_type": "job",
        },
    ),
]
