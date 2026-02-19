from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Dict
from datetime import datetime

class ParticipationBase(BaseModel):
    challenge_id: str
    option_id: int
    participant_name: str
    email: Optional[EmailStr]
    prediction: Dict[str, list]
    amount: float = Field(..., ge=0)
    message: Optional[str]

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