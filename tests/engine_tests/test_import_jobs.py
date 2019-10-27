import pytest
from sauron.engine import Engine
from pprint import pprint
from tests.utils import job_import_module

engine = Engine()


class TestFirstEngineCases:
    def test_can_parse_jobs(self):
        engine.import_jobs(job_import_module)
        assert False
