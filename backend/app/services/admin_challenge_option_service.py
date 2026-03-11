from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Challenge, ChallengeOption
from app.schemas.admin_challenge import (
    AdminChallengeOptionCreate,
    AdminChallengeOptionUpdate,
)


def get_admin_challenge_options(db: Session, challenge_id: str):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    return (
        db.query(ChallengeOption)
        .filter(ChallengeOption.challenge_id == challenge_id)
        .order_by(ChallengeOption.id.asc())
        .all()
    )


def create_admin_challenge_option(
    db: Session,
    challenge_id: str,
    payload: AdminChallengeOptionCreate,
):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    option = ChallengeOption(
        challenge_id=challenge_id,
        name=payload.name,
        description=payload.description,
        subject_type=payload.subject_type,
        answer_type=payload.answer_type,
        number_of_selections=payload.number_of_selections,
        config_json=payload.config_json,
    )

    db.add(option)
    db.commit()
    db.refresh(option)

    return option


def update_admin_challenge_option(
    db: Session,
    option_id: int,
    payload: AdminChallengeOptionUpdate,
):
    option = db.query(ChallengeOption).filter(ChallengeOption.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Challenge option not found")

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(option, field, value)

    db.commit()
    db.refresh(option)

    return option


def delete_admin_challenge_option(db: Session, option_id: int):
    option = db.query(ChallengeOption).filter(ChallengeOption.id == option_id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Challenge option not found")

    db.delete(option)
    db.commit()

    return {"ok": True, "deleted_option_id": option_id}