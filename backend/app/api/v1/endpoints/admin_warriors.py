from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.admin_warrior import (
    AdminWarriorCreate,
    AdminWarriorDetail,
    AdminWarriorListItem,
    AdminWarriorUpdate,
)

from app.services.admin_warrior_service import (
    create_admin_warrior,
    delete_admin_warrior,
    get_admin_warrior_by_id,
    get_admin_warriors,
    update_admin_warrior,
)

router = APIRouter()

UPLOAD_DIR = Path("uploads/warriors")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


@router.get("/", response_model=list[AdminWarriorListItem])
def list_admin_warriors(db: Session = Depends(get_db)):
    return get_admin_warriors(db)


@router.get("/{warrior_id}", response_model=AdminWarriorDetail)
def get_admin_warrior(warrior_id: str, db: Session = Depends(get_db)):
    warrior = get_admin_warrior_by_id(db, warrior_id)

    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")

    return warrior


@router.post("/", response_model=AdminWarriorDetail, status_code=201)
def create_warrior(payload: AdminWarriorCreate, db: Session = Depends(get_db)):
    return create_admin_warrior(db, payload)


@router.patch("/{warrior_id}", response_model=AdminWarriorDetail)
def update_warrior(
    warrior_id: str,
    payload: AdminWarriorUpdate,
    db: Session = Depends(get_db),
):
    return update_admin_warrior(db, warrior_id, payload)


@router.delete("/{warrior_id}")
def delete_warrior(
    warrior_id: str,
    db: Session = Depends(get_db),
):
    return delete_admin_warrior(db, warrior_id)


@router.post("/{warrior_id}/photo", response_model=AdminWarriorDetail)
def upload_warrior_photo(
    warrior_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    warrior = get_admin_warrior_by_id(db, warrior_id)

    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")

    allowed_types = {"image/jpeg", "image/png", "image/webp"}
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid image type")

    extension = Path(file.filename).suffix.lower()
    allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}

    if extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file extension")

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large (max 5MB)")

    unique_id = uuid.uuid4().hex
    filename = f"{warrior_id}_{unique_id}{extension}"
    file_path = UPLOAD_DIR / filename

    if warrior.photo_url:
        old_path = Path(warrior.photo_url.lstrip("/"))
        if old_path.exists():
            old_path.unlink()

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    warrior.photo_url = f"/uploads/warriors/{filename}"

    db.commit()
    db.refresh(warrior)

    return warrior