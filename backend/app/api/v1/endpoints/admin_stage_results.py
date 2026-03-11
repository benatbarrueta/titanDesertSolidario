from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.admin_stage_result import (
    AdminStageResultCreate,
    AdminStageResultDetail,
    AdminStageResultListItem,
    AdminStageResultUpdate,
)
from app.services.admin_stage_result_service import (
    create_admin_stage_result,
    get_admin_stage_result_by_id,
    get_admin_stage_results,
    update_admin_stage_result,
)

router = APIRouter()


@router.get("/", response_model=list[AdminStageResultListItem])
def list_admin_stage_results(
    stage_id: str | None = Query(default=None),
    warrior_id: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    return get_admin_stage_results(db=db, stage_id=stage_id, warrior_id=warrior_id)


@router.get("/{result_id}", response_model=AdminStageResultDetail)
def get_admin_stage_result(result_id: int, db: Session = Depends(get_db)):
    return get_admin_stage_result_by_id(db, result_id)


@router.post("/", response_model=AdminStageResultDetail, status_code=201)
def create_stage_result(
    payload: AdminStageResultCreate,
    db: Session = Depends(get_db),
):
    return create_admin_stage_result(db, payload)


@router.patch("/{result_id}", response_model=AdminStageResultDetail)
def update_stage_result(
    result_id: int,
    payload: AdminStageResultUpdate,
    db: Session = Depends(get_db),
):
    return update_admin_stage_result(db, result_id, payload)