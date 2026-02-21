import json
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import func
from app.db.models import Challenge, ChallengeOption

def get_all_challenges(db: Session):
    # OJO: price es el precio del challenge. Si quieres "min_price" de options, no aplica aquí.
    # Mantengo tu contrato actual: min_price = Challenge.price
    return (
        db.query(
            Challenge.id,
            Challenge.title,
            Challenge.icon,
            Challenge.price.label("min_price"),
            func.count(ChallengeOption.id).label("options_count"),
        )
        .join(ChallengeOption, Challenge.id == ChallengeOption.challenge_id, isouter=True)
        .group_by(Challenge.id)
        .all()
    )


def _serialize_option(o: ChallengeOption) -> dict:
    try:
        cfg = json.loads(o.config_json) if o.config_json else {}
    except Exception:
        cfg = {}

    return {
        "id": o.id,
        "name": o.name,
        "description": o.description or "",
        "subject_type": o.subject_type,
        "answer_type": o.answer_type,
        "number_of_selections": o.number_of_selections,
        "config_json": o.config_json,
        "config": cfg,
    }


def get_challenge_by_id(db: Session, challenge_id: str):
    challenge = (
        db.query(Challenge)
        .options(selectinload(Challenge.options))
        .filter(Challenge.id == challenge_id)
        .first()
    )

    if not challenge:
        return None

    return {
        "id": challenge.id,
        "title": challenge.title,
        "description": challenge.description or "",
        "icon": challenge.icon,
        "price": float(challenge.price),
        "is_active": bool(challenge.is_active),
        "options": [_serialize_option(o) for o in (challenge.options or [])],
    }