from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Any
from datetime import datetime

class ParticipationBase(BaseModel):
    challenge_id: str
    option_id: int
    participant_name: str
    email: EmailStr
    prediction: Any
    amount: float = Field(..., ge=0)
    message: Optional[str] = None

class ParticipationCreate(ParticipationBase):
    pass

class ParticipationResponse(BaseModel):
    id: int
    challenge_id: str
    option_id: int
    amount: float
    created_at: datetime

    class Config:
        from_attributes = True