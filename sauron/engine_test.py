from sauron.engine import Engine
from pprint import pprint

engine = Engine()


@engine.job("First Condition")
def first_condition(session, lower_number=0, greater_number=10):
    result = lower_number < greater_number
    print("#" * 40)
    print("Function called: first_condition")
    print("Function ARGS: ")
    print(f" - lower_number: {lower_number}")
    print(f" - greater_number: {greater_number}")
    print(f"Result EXPECTED: {result}")
    print("#" * 40)
    return result


@engine.job("Second Condition")
def second_condition(session, lower_number=0, greater_number=10):
    result = lower_number
    print("#" * 40)
    print("Function called: second_condition")
    print("Function ARGS: ")
    print(f" - lower_number: {lower_number}")
    print(f" - greater_number: {greater_number}")
    print(f"Result EXPECTED: {result}")
    print("#" * 40)
    return result


@engine.job("The Action")
def print_the_equation(session, lower_number=10, greater_number=20):
    result = None
    print("#" * 40)
    print("Function called: print_the_equation")
    print("Function ARGS: ")
    print(f" - lower_number: {lower_number}")
    print(f" - greater_number: {greater_number}")
    print(f"Result EXPECTED: {result}")
    print("#" * 40)


if __name__ == "__main__":
    jobs = """
        [
            {
                "name": "first_condition",
                "args": {"lower_number": 3, "greater_number": 10},
                "job_type": "condition"
            },
            {
                "name": "print_the_equation",
                "args": {"lower_number": 3, "greater_number": 10},
                "job_type": "action"
            }
        ]
        """.strip()
    session = {"foo": "bar"}
    e = Engine()
    e.run(jobs, session)
    print("PARSED RULES:")
    pprint([j for j in e.parsed_rule])
    print("#" * 40)
    print("final SESSION content:")
    pprint(session)
