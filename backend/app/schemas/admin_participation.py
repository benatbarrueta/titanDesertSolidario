from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AdminParticipationListItem(BaseModel):
    id: int

    challenge_id: str
    option_id: int

    participant_name: str
    email: Optional[str] = None

    amount: float
    message: Optional[str] = None

    payment_status: str

    challenge_title_at_time: str
    stage_name_at_time: Optional[str] = None
    option_name_at_time: Optional[str] = None

    created_at: datetime
    paid_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AdminParticipationDetail(BaseModel):
    id: int

    challenge_id: str
    option_id: int

    participant_name: str
    email: Optional[str] = None

    prediction_json: str

    amount: float
    message: Optional[str] = None

    challenge_title_at_time: str
    challenge_description_at_time: Optional[str] = None
    challenge_price_at_time: float
    challenge_icon_at_time: Optional[str] = None
    challenge_image_url_at_time: Optional[str] = None
    challenge_currency_at_time: str

    stage_id_at_time: Optional[str] = None
    stage_name_at_time: Optional[str] = None

    option_name_at_time: Optional[str] = None
    option_description_at_time: Optional[str] = None

    payment_status: str
    payment_provider: Optional[str] = None
    provider_reference: Optional[str] = None
    paid_at: Optional[datetime] = None

    created_at: datetime

    class Config:
        from_attributes = True