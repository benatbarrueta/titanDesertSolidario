from pydantic import BaseModel
from typing import Optional

class WarriorBase(BaseModel):
    id: str
    dorsal: int
    name: str
    raised_cache: float

    class Config:
        from_attributes = True