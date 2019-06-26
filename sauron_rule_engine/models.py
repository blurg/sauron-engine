from typing import List, Dict, Any
from pydantic import BaseModel, Json


class ConditionModel(BaseModel):
    name: str
    arguments: dict = None


class ActionModel(BaseModel):
    name: str
    arguments: dict = None


class RuleModel(BaseModel):
    conditions: List[ConditionModel]
    actions: List[ActionModel]
