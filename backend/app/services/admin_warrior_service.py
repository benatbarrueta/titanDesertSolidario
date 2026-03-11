from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.db.models import Warrior
from app.schemas.admin_warrior import (
    AdminWarriorCreate,
    AdminWarriorUpdate,
)


def get_admin_warriors(db: Session):
    return (
        db.query(Warrior)
        .order_by(Warrior.dorsal.asc(), Warrior.name.asc())
        .all()
    )


def get_admin_warrior_by_id(db: Session, warrior_id: str):
    warrior = db.query(Warrior).filter(Warrior.id == warrior_id).first()

    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")

    return warrior


def create_admin_warrior(db: Session, payload: AdminWarriorCreate):
    existing_by_id = db.query(Warrior).filter(Warrior.id == payload.id).first()
    if existing_by_id:
        raise HTTPException(status_code=409, detail="Warrior with this id already exists")

    existing_by_dorsal = db.query(Warrior).filter(Warrior.dorsal == payload.dorsal).first()
    if existing_by_dorsal:
        raise HTTPException(status_code=409, detail="Warrior with this dorsal already exists")

    warrior = Warrior(
        id=payload.id,
        dorsal=payload.dorsal,
        name=payload.name,
        photo_url=payload.photo_url,
        raised_cache=payload.raised_cache,
    )

    db.add(warrior)
    db.commit()
    db.refresh(warrior)

    return warrior


def update_admin_warrior(db: Session, warrior_id: str, payload: AdminWarriorUpdate):
    warrior = db.query(Warrior).filter(Warrior.id == warrior_id).first()

    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")

    update_data = payload.model_dump(exclude_unset=True)

    if "dorsal" in update_data:
        existing_by_dorsal = (
            db.query(Warrior)
            .filter(
                Warrior.id != warrior.id,
                Warrior.dorsal == update_data["dorsal"],
            )
            .first()
        )
        if existing_by_dorsal:
            raise HTTPException(status_code=409, detail="Warrior with this dorsal already exists")

    for field, value in update_data.items():
        setattr(warrior, field, value)

    db.commit()
    db.refresh(warrior)

    return warrior


def delete_admin_warrior(db: Session, warrior_id: str):
    warrior = db.query(Warrior).filter(Warrior.id == warrior_id).first()

    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")

    db.delete(warrior)
    db.commit()

    return {"status": "deleted", "id": warrior_id}