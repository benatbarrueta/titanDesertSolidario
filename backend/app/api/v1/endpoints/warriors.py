from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.warrior_repo import get_all_warriors, get_warrior_by_id
from app.schemas.warrior import WarriorBase, WarriorOut
from app.services.warrior_service import get_warriors_with_raised

router = APIRouter()

@router.get("/", response_model=list[WarriorOut])
def list_warriors(db: Session = Depends(get_db)):
    return get_warriors_with_raised(db)

@router.get("/{id}", response_model=WarriorBase)
def get_warrior(id: str, db: Session = Depends(get_db)):
    warrior = get_warrior_by_id(db, id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    return warrior