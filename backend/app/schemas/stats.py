from pydantic import BaseModel

class StatsResponse(BaseModel):
    total_raised: float
    total_participations: int
    currency: str = "EUR"

    class Config:
        from_attributes = True