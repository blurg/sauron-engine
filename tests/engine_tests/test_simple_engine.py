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


class TestFirstEngineCases:
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

    def setup(self):
        session = {"foo": "bar"}
        engine.run(self.test_string, session)
        return engine

    def test_parsed_rules(self):
        engine = self.setup()
        result = engine.parsed_rule
        assert result[1].name == "print_the_equation"
        assert result[1].args == {"lower_number": 3, "greater_number": 10}
        assert result[1].job_type == "action"

    def test_session_content_at_the_end_includes_inital_data(self):
        engine = self.setup()
        assert engine.session.get("foo") == "bar"

    def test_session_includes_all_operations_results_at_the_end(self):
        engine = self.setup()
        assert engine.session.get("results").pop() == {
            "job": "print_the_equation",
            "return": None,
        }
        assert engine.session.get("results").pop() == {
            "job": "first_condition",
            "return": True,
        }

    def test_export_metadata_as_dict(self):
        engine = self.setup()
        metadata = engine.export_metadata()
        assert "print_the_equation" in metadata.keys()
        assert "first_condition" in metadata.keys()
        assert "second_condition" in metadata.keys()
        assert "lower_number" in metadata["second_condition"]["args"].keys()
        assert "greater_number" in metadata["second_condition"]["args"].keys()


class TestEngineRuntimeMetricsCases:
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

    def test_runtime_metrics_zero_values_before_ran(self):
        # given:
        expected_total_runtime = 0
        expected_jobs = {}

        # when
        # engine didn't run
        unran_engine = Engine()
        # then:
        assert (
            unran_engine.runtime_metrics["total_runtime"]
            == expected_total_runtime
        )
        assert unran_engine.runtime_metrics["jobs"] == expected_jobs

    def test_runtime_metrics_with_values_after_ran(self):
        # given:
        expected_metrics_keys = ["jobs", "total_runtime"]
        expected_metrics_jobs_keys = ["first_condition", "print_the_equation"]

        # when:
        engine.run(self.test_string, {})
        metrics_keys = list(engine.runtime_metrics.keys())

        # then:
        assert metrics_keys == expected_metrics_keys
        for job_name in expected_metrics_jobs_keys:
            assert job_name in engine.runtime_metrics["jobs"]
            assert engine.runtime_metrics["jobs"][job_name] > 0
