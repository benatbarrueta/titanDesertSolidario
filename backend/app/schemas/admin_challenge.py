from __future__ import annotations

from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field


class AdminChallengeOptionBase(BaseModel):
    id: int
    challenge_id: str

    name: str
    description: Optional[str] = None

    subject_type: str
    answer_type: str

    number_of_selections: int

    config_json: Optional[str] = None
    config: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True


class AdminChallengeOptionCreate(BaseModel):
    name: str
    description: Optional[str] = None

    subject_type: str = "team"
    answer_type: str = "warrior_pick"

    number_of_selections: int = 1

    config_json: Optional[str] = None


class AdminChallengeOptionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    subject_type: Optional[str] = None
    answer_type: Optional[str] = None

    number_of_selections: Optional[int] = None

    config_json: Optional[str] = None


class AdminChallengeBase(BaseModel):
    id: str
    stage_id: Optional[str] = None

    title: str
    description: str

    price: float
    icon: str

    currency: str = "EUR"
    image_url: Optional[str] = None

    is_active: bool
    is_published: bool
    is_archived: bool

    available_from: Optional[datetime] = None
    available_until: Optional[datetime] = None

    sort_order: int

    class Config:
        from_attributes = True


class AdminChallengeListItem(AdminChallengeBase):
    created_at: datetime
    options_count: int = 0


class AdminChallengeDetail(AdminChallengeBase):
    created_at: datetime
    options: List[AdminChallengeOptionBase] = Field(default_factory=list)


class AdminChallengeCreate(BaseModel):
    id: str
    stage_id: Optional[str] = None

    title: str
    description: str

    price: float
    icon: str

    currency: str = "EUR"
    image_url: Optional[str] = None

    is_active: bool = True
    is_published: bool = False
    is_archived: bool = False

    available_from: Optional[datetime] = None
    available_until: Optional[datetime] = None

    sort_order: int = 0

    options: List[AdminChallengeOptionCreate] = Field(default_factory=list)


class AdminChallengeUpdate(BaseModel):
    stage_id: Optional[str] = None

    title: Optional[str] = None
    description: Optional[str] = None

    price: Optional[float] = None
    icon: Optional[str] = None

    currency: Optional[str] = None
    image_url: Optional[str] = None

    is_active: Optional[bool] = None
    is_published: Optional[bool] = None
    is_archived: Optional[bool] = None

    available_from: Optional[datetime] = None
    available_until: Optional[datetime] = None

    sort_order: Optional[int] = None