from typing import List, Dict, Any
from pydantic import BaseModel, Json


class JobModel(BaseModel):
    job_type: str = "job"
    name: str
    args: Dict[str, Any] = None


class JobsListModel(BaseModel):
    jobs: List[JobModel]


# class ConditionModel(JobModel):
#     job_type: str = "condition"
#     name: str
#     args: Dict[str, Any] = None


# class ActionModel(JobModel):
#     job_type: str = "action"
#     name: str
#     args: Dict[str, Any] = None
