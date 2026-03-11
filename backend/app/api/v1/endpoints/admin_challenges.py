from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.admin_challenge import (
    AdminChallengeCreate,
    AdminChallengeDetail,
    AdminChallengeListItem,
    AdminChallengeUpdate,
)
from app.services.admin_challenge_service import (
    create_admin_challenge,
    get_admin_challenge_by_id,
    get_admin_challenges,
    update_admin_challenge,
)

router = APIRouter()


@router.get("/", response_model=list[AdminChallengeListItem])
def list_admin_challenges(db: Session = Depends(get_db)):
    return get_admin_challenges(db)


@router.get("/{challenge_id}", response_model=AdminChallengeDetail)
def get_admin_challenge(challenge_id: str, db: Session = Depends(get_db)):
    return get_admin_challenge_by_id(db, challenge_id)


@router.post("/", response_model=AdminChallengeDetail, status_code=201)
def create_challenge(payload: AdminChallengeCreate, db: Session = Depends(get_db)):
    return create_admin_challenge(db, payload)


@router.patch("/{challenge_id}", response_model=AdminChallengeDetail)
def update_challenge(
    challenge_id: str,
    payload: AdminChallengeUpdate,
    db: Session = Depends(get_db),
):
    return update_admin_challenge(db, challenge_id, payload)