from __future__ import annotations

import json
from sqlalchemy.orm import Session

from app.repositories.warrior_repo import get_all_warriors
from app.db.models import Participation, ChallengeOption
from app.schemas.warrior import WarriorOut


def _safe_load_prediction(prediction_json: str | None) -> dict:
    if not prediction_json:
        return {}
    try:
        data = json.loads(prediction_json)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def get_warriors_with_raised(db: Session):
    warriors = get_all_warriors(db)

    return [
        WarriorOut(
            id=w.id,
            dorsal=w.dorsal,
            name=w.name,
            raised=float(w.raised_cache or 0.0),
            photo_url=w.photo_url,
        )
        for w in warriors
    ]