from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Participation


def get_admin_participations(
    db: Session,
    challenge_id: str | None = None,
    email: str | None = None,
    participant_name: str | None = None,
):
    query = db.query(Participation)

    if challenge_id:
        query = query.filter(Participation.challenge_id == challenge_id)

    if email:
        query = query.filter(Participation.email.ilike(f"%{email}%"))

    if participant_name:
        query = query.filter(Participation.participant_name.ilike(f"%{participant_name}%"))

    return query.order_by(Participation.created_at.desc()).all()


def get_admin_participation_by_id(db: Session, participation_id: int):
    participation = (
        db.query(Participation)
        .filter(Participation.id == participation_id)
        .first()
    )

    if not participation:
        raise HTTPException(status_code=404, detail="Participation not found")

    return participation