from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Stage
from app.schemas.admin_stage import (
    AdminStageCreate,
    AdminStageUpdate,
)


def get_admin_stages(db: Session):
    return (
        db.query(Stage)
        .order_by(Stage.sort_order.asc(), Stage.stage_number.asc())
        .all()
    )


def get_admin_stage_by_id(db: Session, stage_id: str):
    stage = db.query(Stage).filter(Stage.id == stage_id).first()

    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")

    return stage


def create_admin_stage(db: Session, payload: AdminStageCreate):
    existing = db.query(Stage).filter(Stage.id == payload.id).first()
    if existing:
        raise HTTPException(status_code=409, detail="Stage with this id already exists")

    stage_number_exists = (
        db.query(Stage)
        .filter(
            Stage.edition_year == payload.edition_year,
            Stage.stage_number == payload.stage_number,
        )
        .first()
    )
    if stage_number_exists:
        raise HTTPException(
            status_code=409,
            detail="Stage number already exists for this edition year",
        )

    stage = Stage(
        id=payload.id,
        edition_year=payload.edition_year,
        stage_number=payload.stage_number,
        name=payload.name,
        start_location=payload.start_location,
        finish_location=payload.finish_location,
        distance_km=payload.distance_km,
        elevation_gain_m=payload.elevation_gain_m,
        is_loop=payload.is_loop,
        is_marathon_sector=payload.is_marathon_sector,
        has_navigation_sector=payload.has_navigation_sector,
        has_timed_challenge=payload.has_timed_challenge,
        notes=payload.notes,
        is_published=payload.is_published,
        is_open_for_contributions=payload.is_open_for_contributions,
        is_archived=payload.is_archived,
        visible_from=payload.visible_from,
        visible_until=payload.visible_until,
        sort_order=payload.sort_order,
    )

    db.add(stage)
    db.commit()
    db.refresh(stage)

    return stage


def update_admin_stage(db: Session, stage_id: str, payload: AdminStageUpdate):
    stage = db.query(Stage).filter(Stage.id == stage_id).first()

    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")

    update_data = payload.model_dump(exclude_unset=True)

    if "stage_number" in update_data or "edition_year" in update_data:
        next_stage_number = update_data.get("stage_number", stage.stage_number)
        next_edition_year = update_data.get("edition_year", stage.edition_year)

        stage_number_exists = (
            db.query(Stage)
            .filter(
                Stage.id != stage.id,
                Stage.edition_year == next_edition_year,
                Stage.stage_number == next_stage_number,
            )
            .first()
        )
        if stage_number_exists:
            raise HTTPException(
                status_code=409,
                detail="Stage number already exists for this edition year",
            )

    for field, value in update_data.items():
        setattr(stage, field, value)

    db.commit()
    db.refresh(stage)

    return stage