from pydantic import BaseModel
from typing import List, Optional

class ChallengeOptionBase(BaseModel):
    id: int
    name: str
    description: str
    type: str
    number_of_selections: int

    class Config:
        from_attributes = True

class ChallengeBase(BaseModel):
    id: str
    title: str
    icon: str
    price: float
    is_active: bool

    class Config:
        from_attributes = True

class ChallengeDetail(ChallengeBase):
    description: str
    options: List[ChallengeOptionBase]