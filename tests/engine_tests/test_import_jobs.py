from sauron.engine import Engine
from tests.utils import job_import_module, job_import_module_verbose

engine = Engine()


class TestFirstEngineCases:
    def test_can_parse_two_jobs(self):
        engine.import_jobs(job_import_module)
        jobs = engine.callables_collected
        assert len(jobs) == 2
        assert list(jobs.keys()) == ["always_true", "times_two"]

    def test_can_parse_jobs_with_verbose_names(self):
        engine.import_jobs(job_import_module_verbose)
        jobs = engine.callables_collected
        assert len(jobs) == 2
        assert [job["verbose_name"] for job in jobs.values()] == [
            "True Always Is",
            "Double that",
        ]
