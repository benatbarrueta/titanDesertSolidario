from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AdminWarriorBase(BaseModel):
    id: str
    dorsal: int
    name: str
    raised_cache: float
    photo_url: Optional[str] = None

    class Config:
        from_attributes = True


class AdminWarriorListItem(AdminWarriorBase):
    created_at: datetime


class AdminWarriorDetail(AdminWarriorBase):
    created_at: datetime


class AdminWarriorCreate(BaseModel):
    id: str
    dorsal: int
    name: str
    raised_cache: float = 0.0
    photo_url: Optional[str] = None


class AdminWarriorUpdate(BaseModel):
    dorsal: Optional[int] = None
    name: Optional[str] = None
    raised_cache: Optional[float] = None
    photo_url: Optional[str] = None