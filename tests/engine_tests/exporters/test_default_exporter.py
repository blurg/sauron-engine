from sauron.exporters import DefaultExporter
import pytest
from sauron.engine import Engine
from pprint import pprint

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


class TestDefaultExporter:
    def setup(self):
        exporter = DefaultExporter()
        self.exported_jobs = exporter.export_jobs(engine.callables_collected)
        self.exported_jobs_as_json = exporter.export_jobs(
            engine.callables_collected, json=True
        )

    def test_can_export_simple_engine(self):
        assert type(self.exported_jobs) is dict

    def test_can_export_simple_engine_as_json(self):
        assert type(self.exported_jobs_as_json) is str

    def test_exported_data_has_three_jobs(self):
        assert len(self.exported_jobs) == 3

    def test_exported_data_has_job_names_accurate(self):
        assert [name for name in self.exported_jobs.keys()] == [
            "first_condition",
            "second_condition",
            "print_the_equation",
        ]

    def test_exported_data_has_job_verbose_names_accurate(self):
        assert [
            value["name"] for name, value in self.exported_jobs.items()
        ] == ["First Condition", "Second Condition", "The Action"]
