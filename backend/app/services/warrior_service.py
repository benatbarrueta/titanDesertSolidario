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

    # acumulador por warrior_id
    warrior_raised: dict[str, float] = {}

    # Traemos option.answer_type para filtrar SOLO warrior_pick
    rows = (
        db.query(Participation, ChallengeOption)
        .join(ChallengeOption, Participation.option_id == ChallengeOption.id)
        .all()
    )

    for participation, option in rows:
        # Solo tiene sentido repartir recaudación por corredor si el answer es warrior_pick
        if option.answer_type != "warrior_pick":
            continue

        prediction = _safe_load_prediction(participation.prediction_json)
        selections = prediction.get("selections") or []

        if not isinstance(selections, list) or len(selections) == 0:
            continue

        # Opcional: filtra solo strings
        selections = [s for s in selections if isinstance(s, str) and s.strip()]
        if not selections:
            continue

        # Evitar duplicados por si viniera mal
        unique_selections = list(dict.fromkeys(selections))
        if len(unique_selections) == 0:
            continue

        amount_per_warrior = float(participation.amount) / len(unique_selections)

        for warrior_id in unique_selections:
            warrior_raised[warrior_id] = warrior_raised.get(warrior_id, 0.0) + amount_per_warrior

    # Construir respuesta con 0.0 por defecto
    return [
        WarriorOut(
            id=w.id,
            dorsal=w.dorsal,
            name=w.name,
            raised=float(warrior_raised.get(w.id, 0.0)),
        )
        for w in warriors
    ]