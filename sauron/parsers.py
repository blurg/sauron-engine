import json
from json.decoder import JSONDecodeError
from typing import List, Type
from sauron.models import JobModel, JobsListModel


class DefaultParser:
    single_model: Type[JobModel] = JobModel

    def parse_single_job(self, job_dict):
        """
        Method that know how to parse a single job dictionary
        """
        return self.single_model(**job_dict)

    def parse_jobs_from_list(self, jobs_input):
        """
        Method that know how to parse a list for jobs
        """
        parsed_jobs = []
        for raw_job in jobs_input:
            parsed_job = self.parse_single_job(raw_job)
            parsed_jobs.append(parsed_job)
        return parsed_jobs

    def parse_jobs_from_string(self, jobs_input):
        """
        Method that know how to parse a list for jobs described by a
        json-string with the list of jobs
        """
        try:
            jobs_list = json.loads(jobs_input)
        except JSONDecodeError:
            raise ValueError("jobs param is not a valid json string")
        else:
            return self.parse_jobs_from_list(jobs_list)

    def parse(self, jobs_input):
        """
        Main method called to parse any jobs
        """
        jobs_list_data: List[Type[JobModel]] = []
        if isinstance(jobs_input, str):
            jobs_list_data = self.parse_jobs_from_string(jobs_input)
        elif isinstance(jobs_input, list):
            # jobs_input is a python list
            jobs_list_data = self.parse_jobs_from_list(jobs_input)
        else:
            raise ValueError("jobs param must be a list or json-string")
        return jobs_list_data


def dummy_test():
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
    """
    jobs = jobs.strip()
    p = DefaultParser()
    p.parse(jobs)


if __name__ == "__main__":
    dummy_test()
