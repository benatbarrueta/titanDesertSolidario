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

    # SNAPSHOT DEL RETO
    challenge_title_at_time: Optional[str] = None
    challenge_price_at_time: Optional[float] = None
    challenge_icon_at_time: Optional[str] = None

    # SNAPSHOT DE ETAPA
    stage_id_at_time: Optional[str] = None
    stage_name_at_time: Optional[str] = None

    # SNAPSHOT DE OPCIÓN
    option_name_at_time: Optional[str] = None

    class Config:
        from_attributes = True