from typing import Any, Dict, List

from pydantic import BaseModel


# Generic Models
class JobModel(BaseModel):
    job_type: str = "job"
    name: str
    args: Dict[str, Any] = None


# Rule Engine Models
class ConditionModel(JobModel):
    job_type: str = "condition"


class ActionModel(JobModel):
    job_type: str = "action"


class RuleModel(BaseModel):
    conditions: List[ConditionModel]
    actions: List[ActionModel]
