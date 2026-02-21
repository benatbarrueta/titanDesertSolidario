from pydantic import BaseModel


class StageOut(BaseModel):
    id: str
    edition_year: int
    stage_number: int
    name: str
    start_location: str | None = None
    finish_location: str | None = None
    distance_km: float
    elevation_gain_m: int | None = None
    is_loop: bool
    is_marathon_sector: bool
    has_navigation_sector: bool
    has_timed_challenge: bool
    notes: str | None = None

    class Config:
        from_attributes = True