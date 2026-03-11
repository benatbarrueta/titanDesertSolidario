import json

from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.db.models import Participation, Challenge, ChallengeOption, Warrior
from app.schemas.participation import ParticipationCreate
from app.repositories.participation_repo import create_participation


def _get_warrior_allocations(db: Session, participation_data: ParticipationCreate):
    """
    Devuelve una lista de tuplas: [(warrior_obj, amount_to_add), ...]
    Regla:
    - si hay warrior_id => todo el importe a ese warrior
    - si no, si hay selections => repartir a partes iguales entre selections únicas válidas
    - si no hay warrior identificable => []
    """
    prediction = participation_data.prediction or {}
    amount = float(participation_data.amount or 0)

    warrior_id = prediction.get("warrior_id")
    if isinstance(warrior_id, str) and warrior_id.strip():
        warrior = db.query(Warrior).filter(Warrior.id == warrior_id).first()
        if warrior:
            return [(warrior, amount)]
        return []

    selections = prediction.get("selections", [])
    if isinstance(selections, list) and selections:
        unique_ids = []
        seen = set()

        for wid in selections:
            if isinstance(wid, str) and wid.strip() and wid not in seen:
                seen.add(wid)
                unique_ids.append(wid)

        if not unique_ids:
            return []

        warriors = db.query(Warrior).filter(Warrior.id.in_(unique_ids)).all()
        warriors_by_id = {w.id: w for w in warriors}

        valid_warriors = [warriors_by_id[wid] for wid in unique_ids if wid in warriors_by_id]
        if not valid_warriors:
            return []

        split_amount = amount / len(valid_warriors)
        return [(w, split_amount) for w in valid_warriors]

    return []


def create_new_participation(
    db: Session,
    participation_data: ParticipationCreate,
):
    challenge = (
        db.query(Challenge)
        .filter(Challenge.id == participation_data.challenge_id)
        .first()
    )

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    option = (
        db.query(ChallengeOption)
        .filter(
            ChallengeOption.id == participation_data.option_id,
            ChallengeOption.challenge_id == challenge.id,
        )
        .first()
    )

    if not option:
        raise HTTPException(status_code=404, detail="Challenge option not found")

    participation = Participation(
        challenge_id=participation_data.challenge_id,
        option_id=participation_data.option_id,
        participant_name=participation_data.participant_name,
        email=participation_data.email,
        prediction_json=json.dumps(participation_data.prediction, ensure_ascii=False),
        amount=participation_data.amount,
        message=participation_data.message,
    )

    created_participation = create_participation(db, participation, challenge, option)

    # Actualizar raised_cache del/los warrior(s)
    allocations = _get_warrior_allocations(db, participation_data)
    if allocations:
        for warrior, amount_to_add in allocations:
            warrior.raised_cache = float(warrior.raised_cache or 0) + float(amount_to_add)

        db.commit()

    return created_participation