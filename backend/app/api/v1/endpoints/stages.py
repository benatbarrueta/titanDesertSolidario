from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Stage
from app.schemas.stage import StageOut

router = APIRouter()

@router.get("/", response_model=list[StageOut])
def list_stages(db: Session = Depends(get_db)):
    return db.query(Stage).order_by(Stage.stage_number.asc()).all()

@router.get("/{stage_id}", response_model=StageOut)
def get_stage(stage_id: str, db: Session = Depends(get_db)):
    stage = db.query(Stage).filter(Stage.id == stage_id).first()
    if not stage:
        raise HTTPException(status_code=404, detail="Stage not found")
    return stage