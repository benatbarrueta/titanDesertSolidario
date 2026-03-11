from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class StageOut(BaseModel):
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

    # NUEVOS CAMPOS ADMIN
    is_published: bool = False
    is_open_for_contributions: bool = False
    is_archived: bool = False

    visible_from: Optional[datetime] = None
    visible_until: Optional[datetime] = None

    sort_order: int = 0

    class Config:
        from_attributes = True