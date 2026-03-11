from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.admin_challenge import (
    AdminChallengeOptionBase,
    AdminChallengeOptionCreate,
    AdminChallengeOptionUpdate,
)
from app.services.admin_challenge_option_service import (
    create_admin_challenge_option,
    delete_admin_challenge_option,
    get_admin_challenge_options,
    update_admin_challenge_option,
)

router = APIRouter()


@router.get("/{challenge_id}", response_model=list[AdminChallengeOptionBase])
def list_admin_challenge_options(
    challenge_id: str,
    db: Session = Depends(get_db),
):
    return get_admin_challenge_options(db, challenge_id)


@router.post("/{challenge_id}", response_model=AdminChallengeOptionBase, status_code=201)
def create_option(
    challenge_id: str,
    payload: AdminChallengeOptionCreate,
    db: Session = Depends(get_db),
):
    return create_admin_challenge_option(db, challenge_id, payload)


@router.patch("/{option_id}", response_model=AdminChallengeOptionBase)
def update_option(
    option_id: int,
    payload: AdminChallengeOptionUpdate,
    db: Session = Depends(get_db),
):
    return update_admin_challenge_option(db, option_id, payload)


@router.delete("/{option_id}")
def delete_option(
    option_id: int,
    db: Session = Depends(get_db),
):
    return delete_admin_challenge_option(db, option_id)