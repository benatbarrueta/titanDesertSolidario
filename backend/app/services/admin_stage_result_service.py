from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import StageResult, Stage, Warrior
from app.schemas.admin_stage_result import (
    AdminStageResultCreate,
    AdminStageResultUpdate,
)


def _ensure_stage_exists(db: Session, stage_id: str):
    stage = db.query(Stage).filter(Stage.id == stage_id).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    return stage


def _ensure_warrior_exists(db: Session, warrior_id: str):
    warrior = db.query(Warrior).filter(Warrior.id == warrior_id).first()
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    return warrior


def get_admin_stage_results(
    db: Session,
    stage_id: str | None = None,
    warrior_id: str | None = None,
):
    query = db.query(StageResult)

    if stage_id:
        query = query.filter(StageResult.stage_id == stage_id)

    if warrior_id:
        query = query.filter(StageResult.warrior_id == warrior_id)

    return query.order_by(StageResult.created_at.desc()).all()


def get_admin_stage_result_by_id(db: Session, result_id: int):
    result = db.query(StageResult).filter(StageResult.id == result_id).first()

    if not result:
        raise HTTPException(status_code=404, detail="Stage result not found")

    return result


def create_admin_stage_result(db: Session, payload: AdminStageResultCreate):
    _ensure_stage_exists(db, payload.stage_id)
    _ensure_warrior_exists(db, payload.warrior_id)

    existing = (
        db.query(StageResult)
        .filter(
            StageResult.stage_id == payload.stage_id,
            StageResult.warrior_id == payload.warrior_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=409,
            detail="A result for this stage and warrior already exists",
        )

    result = StageResult(
        stage_id=payload.stage_id,
        warrior_id=payload.warrior_id,
        position=payload.position,
        time_seconds=payload.time_seconds,
        punctures=payload.punctures,
        mechanical_issues=payload.mechanical_issues,
        crashes=payload.crashes,
        did_finish=payload.did_finish,
        received_medical_help=payload.received_medical_help,
        notes=payload.notes,
    )

    db.add(result)
    db.commit()
    db.refresh(result)

    return result


def update_admin_stage_result(db: Session, result_id: int, payload: AdminStageResultUpdate):
    result = db.query(StageResult).filter(StageResult.id == result_id).first()

    if not result:
        raise HTTPException(status_code=404, detail="Stage result not found")

    update_data = payload.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(result, field, value)

    db.commit()
    db.refresh(result)

    return result