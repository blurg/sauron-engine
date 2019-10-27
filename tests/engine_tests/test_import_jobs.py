from typing import List
import pytest
from sauron.engine import Engine
from pprint import pprint
from tests.utils import job_import_module

engine = Engine()


class TestFirstEngineCases:
    def test_can_parse_two_jobs(self):
        engine.import_jobs(job_import_module)
        jobs = engine.callables_collected
        print(jobs)
        assert len(jobs) == 2
        assert [job for job in jobs.keys()] == ["always_true", "times_two"]
