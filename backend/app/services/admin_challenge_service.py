from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.db.models import Challenge, ChallengeOption, Stage
from app.schemas.admin_challenge import (
    AdminChallengeCreate,
    AdminChallengeUpdate,
)


def _ensure_stage_exists_if_provided(db: Session, stage_id: str | None):
    if stage_id is None:
        return

    stage = db.query(Stage).filter(Stage.id == stage_id).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")


def get_admin_challenges(db: Session):
    challenges = (
        db.query(Challenge)
        .options(joinedload(Challenge.options))
        .order_by(Challenge.sort_order.asc(), Challenge.title.asc())
        .all()
    )

    for challenge in challenges:
        challenge.options_count = len(challenge.options)

    return challenges


def get_admin_challenge_by_id(db: Session, challenge_id: str):
    challenge = (
        db.query(Challenge)
        .options(joinedload(Challenge.options))
        .filter(Challenge.id == challenge_id)
        .first()
    )

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    return challenge


def create_admin_challenge(db: Session, payload: AdminChallengeCreate):
    existing = db.query(Challenge).filter(Challenge.id == payload.id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Challenge with this id already exists")

    _ensure_stage_exists_if_provided(db, payload.stage_id)

    challenge = Challenge(
        id=payload.id,
        stage_id=payload.stage_id,
        title=payload.title,
        description=payload.description,
        price=payload.price,
        icon=payload.icon,
        currency=payload.currency,
        image_url=payload.image_url,
        is_active=payload.is_active,
        is_published=payload.is_published,
        is_archived=payload.is_archived,
        available_from=payload.available_from,
        available_until=payload.available_until,
        sort_order=payload.sort_order,
    )

    db.add(challenge)
    db.flush()

    for option_payload in payload.options:
        option = ChallengeOption(
            challenge_id=challenge.id,
            name=option_payload.name,
            description=option_payload.description,
            subject_type=option_payload.subject_type,
            answer_type=option_payload.answer_type,
            number_of_selections=option_payload.number_of_selections,
            config_json=option_payload.config_json,
        )
        db.add(option)

    db.commit()

    created = (
        db.query(Challenge)
        .options(joinedload(Challenge.options))
        .filter(Challenge.id == challenge.id)
        .first()
    )

    return created


def update_admin_challenge(db: Session, challenge_id: str, payload: AdminChallengeUpdate):
    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()

    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    update_data = payload.model_dump(exclude_unset=True)

    if "stage_id" in update_data:
        _ensure_stage_exists_if_provided(db, update_data["stage_id"])

    for field, value in update_data.items():
        setattr(challenge, field, value)

    db.commit()

    updated = (
        db.query(Challenge)
        .options(joinedload(Challenge.options))
        .filter(Challenge.id == challenge.id)
        .first()
    )

    return updated