from blinker.base import NamedSignal

from sauron.engine import Engine

engine = Engine()


@engine.job("First Condition", type="condition")
def first_condition(session, lower_number: int = 0, greater_number: int = 10):
    result = lower_number < greater_number
    return result


@engine.job("Second Condition")
def second_condition(session, lower_number: int = 0, greater_number: int = 10):
    result = lower_number
    return result


@engine.job("The Action", type="action")
def print_the_equation(
    session, lower_number: int = 10, greater_number: int = 20
):
    result = None
    print("#" * 40)
    print("Function called: print_the_equation")
    print("Function ARGS: ")
    print(f" - lower_number: {lower_number}")
    print(f" - greater_number: {greater_number}")
    print(f"Result EXPECTED: {result}")
    print("#" * 40)


class TestSignalCases:
    test_string = """
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
    """

    signal_names = [
        "pre_engine_run",
        "post_engine_run",
        "pre_job_call",
        "post_job_call",
    ]

    def setup(self):
        session = {"foo": "bar"}
        engine.run(self.test_string, session)
        return engine

    def test_engine_initialized(self):
        # given:
        expected_signal_names = self.signal_names

        # when:
        engine = self.setup()

        # then:
        assert list(engine.signals.keys()) == expected_signal_names
        for signal_name in expected_signal_names:
            signal_obj = engine.signals[signal_name]
            assert signal_obj is not None
            assert isinstance(signal_obj, NamedSignal)

    def test_signal_connection(self):
        signal_name = "pre_engine_run"

        for signal_name in self.signal_names:
            engine = self.setup()
            hook = engine.get_signal(signal_name)

            def hook_call_back(sender, **kwargs):
                ...

            # when:
            hook.connect(hook_call_back, sender=engine)
            expected_receiver_id = [k for k, v in hook.receivers.items()][0]

            # then:
            assert hook.name == signal_name
            assert len(hook.receivers) == 1
            assert id(hook_call_back) == expected_receiver_id
