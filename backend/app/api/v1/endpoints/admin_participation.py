from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.admin_participation import (
    AdminParticipationDetail,
    AdminParticipationListItem,
)
from app.services.admin_participation_service import (
    get_admin_participation_by_id,
    get_admin_participations,
)

router = APIRouter()


@router.get("/", response_model=list[AdminParticipationListItem])
def list_admin_participations(
    challenge_id: str | None = Query(default=None),
    email: str | None = Query(default=None),
    participant_name: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return get_admin_participations(
        db=db,
        challenge_id=challenge_id,
        email=email,
        participant_name=participant_name,
    )


@router.get("/{participation_id}", response_model=AdminParticipationDetail)
def get_admin_participation(
    participation_id: int,
    db: Session = Depends(get_db),
):
    return get_admin_participation_by_id(db, participation_id)