from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ChallengeOptionBase(BaseModel):
    id: int
    name: str
    description: str

    # NUEVO motor
    subject_type: str
    answer_type: str

    number_of_selections: int

    # Opcional: si quieres exponerlo crudo (texto JSON)
    config_json: Optional[str] = None

    # Recomendado para frontend: dict parseado
    config: Dict[str, Any] = {}

    class Config:
        from_attributes = True


class ChallengeBase(BaseModel):
    id: str
    title: str
    icon: str
    price: float
    is_active: bool

    class Config:
        from_attributes = True


class ChallengeDetail(ChallengeBase):
    description: str
    options: List[ChallengeOptionBase]


class ChallengeListItem(BaseModel):
    id: str
    title: str
    icon: str
    min_price: float
    options_count: int

    class Config:
        from_attributes = True