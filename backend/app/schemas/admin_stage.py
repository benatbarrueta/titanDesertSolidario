from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AdminStageBase(BaseModel):
    id: str
    edition_year: int
    stage_number: int
    name: str

    start_location: Optional[str] = None
    finish_location: Optional[str] = None

    distance_km: float
    elevation_gain_m: Optional[int] = None

    is_loop: bool
    is_marathon_sector: bool
    has_navigation_sector: bool
    has_timed_challenge: bool

    notes: Optional[str] = None

    is_published: bool
    is_open_for_contributions: bool
    is_archived: bool

    visible_from: Optional[datetime] = None
    visible_until: Optional[datetime] = None

    sort_order: int

    class Config:
        from_attributes = True


class AdminStageListItem(AdminStageBase):
    created_at: datetime


class AdminStageDetail(AdminStageBase):
    created_at: datetime


class AdminStageUpdate(BaseModel):
    edition_year: Optional[int] = None
    stage_number: Optional[int] = None
    name: Optional[str] = None

    start_location: Optional[str] = None
    finish_location: Optional[str] = None

    distance_km: Optional[float] = None
    elevation_gain_m: Optional[int] = None

    is_loop: Optional[bool] = None
    is_marathon_sector: Optional[bool] = None
    has_navigation_sector: Optional[bool] = None
    has_timed_challenge: Optional[bool] = None

    notes: Optional[str] = None

    is_published: Optional[bool] = None
    is_open_for_contributions: Optional[bool] = None
    is_archived: Optional[bool] = None

    visible_from: Optional[datetime] = None
    visible_until: Optional[datetime] = None

    sort_order: Optional[int] = None


class AdminStageCreate(BaseModel):
    id: str
    edition_year: int = 2026
    stage_number: int
    name: str

    start_location: Optional[str] = None
    finish_location: Optional[str] = None

    distance_km: float
    elevation_gain_m: Optional[int] = None

    is_loop: bool = False
    is_marathon_sector: bool = False
    has_navigation_sector: bool = False
    has_timed_challenge: bool = False

    notes: Optional[str] = None

    is_published: bool = False
    is_open_for_contributions: bool = False
    is_archived: bool = False

    visible_from: Optional[datetime] = None
    visible_until: Optional[datetime] = None

    sort_order: int = 0