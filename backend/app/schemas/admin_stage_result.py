from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AdminStageResultBase(BaseModel):
    id: int
    stage_id: str
    warrior_id: str

    position: Optional[int] = None
    time_seconds: Optional[int] = None

    punctures: int
    mechanical_issues: int
    crashes: int

    did_finish: bool
    received_medical_help: bool

    notes: Optional[str] = None

    class Config:
        from_attributes = True


class AdminStageResultListItem(AdminStageResultBase):
    created_at: datetime


class AdminStageResultDetail(AdminStageResultBase):
    created_at: datetime


class AdminStageResultCreate(BaseModel):
    stage_id: str
    warrior_id: str

    position: Optional[int] = None
    time_seconds: Optional[int] = None

    punctures: int = 0
    mechanical_issues: int = 0
    crashes: int = 0

    did_finish: bool = True
    received_medical_help: bool = False

    notes: Optional[str] = None


class AdminStageResultUpdate(BaseModel):
    position: Optional[int] = None
    time_seconds: Optional[int] = None

    punctures: Optional[int] = None
    mechanical_issues: Optional[int] = None
    crashes: Optional[int] = None

    did_finish: Optional[bool] = None
    received_medical_help: Optional[bool] = None

    notes: Optional[str] = None