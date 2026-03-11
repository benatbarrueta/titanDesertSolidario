from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.admin_stage import (
    AdminStageCreate,
    AdminStageDetail,
    AdminStageListItem,
    AdminStageUpdate,
)
from app.services.admin_stage_service import (
    create_admin_stage,
    get_admin_stage_by_id,
    get_admin_stages,
    update_admin_stage,
)

router = APIRouter()


@router.get("/", response_model=list[AdminStageListItem])
def list_admin_stages(db: Session = Depends(get_db)):
    return get_admin_stages(db)


@router.get("/{stage_id}", response_model=AdminStageDetail)
def get_admin_stage(stage_id: str, db: Session = Depends(get_db)):
    return get_admin_stage_by_id(db, stage_id)


@router.post("/", response_model=AdminStageDetail, status_code=201)
def create_stage(payload: AdminStageCreate, db: Session = Depends(get_db)):
    return create_admin_stage(db, payload)


@router.patch("/{stage_id}", response_model=AdminStageDetail)
def update_stage(
    stage_id: str,
    payload: AdminStageUpdate,
    db: Session = Depends(get_db),
):
    return update_admin_stage(db, stage_id, payload)