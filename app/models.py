from pydantic import BaseModel
from typing import Optional

class Observation(BaseModel):
    ticket_id: int
    ticket_text: str
    status: str
    category: Optional[str] = None   # ✅ ADD THIS


# What the agent sends
class Action(BaseModel):
    action_type: str   # classify / resolve
    value: Optional[str] = None  # e.g., "billing"


# What environment returns as reward
class Reward(BaseModel):
    score: float   # between 0.0 and 1.0