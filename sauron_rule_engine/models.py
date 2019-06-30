from typing import List, Dict, Any
from pydantic import BaseModel, Json


class ConditionModel(BaseModel):
    name: str
    args: Dict[str, Any] = None


class ActionModel(BaseModel):
    name: str
    args: Dict[str, Any] = None


class RuleModel(BaseModel):
    conditions: List[ConditionModel]
    actions: List[ActionModel]
