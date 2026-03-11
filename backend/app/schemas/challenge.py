from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ChallengeOptionBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None

    subject_type: str
    answer_type: str

    number_of_selections: int

    config_json: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True


class ChallengeBase(BaseModel):
    id: str
    title: str
    icon: Optional[str] = None
    price: float
    is_active: bool

    # NUEVOS CAMPOS
    stage_id: Optional[str] = None
    description: Optional[str] = None
    currency: str = "EUR"
    image_url: Optional[str] = None

    is_published: bool = False
    is_archived: bool = False

    available_from: Optional[datetime] = None
    available_until: Optional[datetime] = None

    sort_order: int = 0

    class Config:
        from_attributes = True


class ChallengeDetail(ChallengeBase):
    description: Optional[str] = None
    options: List[ChallengeOptionBase]


class ChallengeListItem(BaseModel):
    id: str
    title: str
    icon: Optional[str] = None
    min_price: float
    options_count: int

    class Config:
        from_attributes = True