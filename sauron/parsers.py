from json.decoder import JSONDecodeError
from typing import List, Type, Union

from ruamel.yaml import YAML

from sauron.models import JobModel


class DefaultParser:
    single_model: Type[JobModel] = JobModel

    def __init__(self):
        self.yaml = YAML(typ="safe")

    def _parse_single_job(self, job_dict) -> JobModel:
        """
        Method that know how to parse a single job dictionary
        """
        return self.single_model(**job_dict)

    def _parse_jobs_from_list(self, jobs_input) -> List[JobModel]:
        """
        Method that know how to parse a list for jobs
        """
        parsed_jobs: List = []
        for raw_job in jobs_input:
            current_job: JobModel = self._parse_single_job(raw_job)
            parsed_jobs.append(current_job)
        return parsed_jobs

    def _parse_jobs_from_string(self, jobs_input) -> List[JobModel]:
        """
        Method that know how to parse a list for jobs described by a
        json-string with the list of jobs
        """
        try:
            jobs: list = self.yaml.load(jobs_input)
        except JSONDecodeError:
            raise ValueError("jobs param is not a valid json string") from None
        else:
            return self._parse_jobs_from_list(jobs)

    def parse(self, jobs_input) -> List[JobModel]:
        """
        Main method called to parse any jobs
        """
        jobs_list_data: List[JobModel] = []
        if isinstance(jobs_input, str):
            jobs_list_data = self._parse_jobs_from_string(jobs_input)
        elif isinstance(jobs_input, list):
            # jobs_input is a python list
            jobs_list_data = self._parse_jobs_from_list(jobs_input)
        else:
            raise ValueError("jobs param must be a list or json-string")
        return jobs_list_data


class RuleEngineParser(DefaultParser):
    single_model: Type[JobModel] = JobModel

    def __init__(self):
        self.yaml = YAML(typ="safe")

    def _parse_jobs_from_string(self, jobs_input: str) -> List[JobModel]:
        """
        Method that know how to parse a list for jobs described by a
        json-string with the list of jobs
        """
        try:
            decoded_jobs: dict = self.yaml.load(jobs_input)
            jobs: list = decoded_jobs["conditions"] + decoded_jobs["actions"]
        except JSONDecodeError:
            raise ValueError("jobs param is not a valid json string") from None
        else:
            return self._parse_jobs_from_list(jobs)

    def parse(self, jobs_input: Union[List, str]) -> List[JobModel]:
        """
        Main method called to parse any jobs
        """
        jobs_list_data: List[JobModel] = []
        if isinstance(jobs_input, str):
            jobs_list_data = self._parse_jobs_from_string(jobs_input)
        elif isinstance(jobs_input, list):
            # jobs_input is a python list
            jobs_list_data = self._parse_jobs_from_list(jobs_input)
        elif isinstance(jobs_input, dict):
            # jobs_input is a python list
            jobs_list_data = self._parse_jobs_from_string(str(jobs_input))
        else:
            raise ValueError("jobs param must be a list or json-string")
        return jobs_list_data
