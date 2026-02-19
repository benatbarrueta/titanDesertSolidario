from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.participation_service import create_new_participation
from app.schemas.participation import ParticipationCreate, ParticipationResponse

router = APIRouter()

@router.post("/", response_model=ParticipationResponse)
def create_participation(
    participation: ParticipationCreate, db: Session = Depends(get_db)
):
    return create_new_participation(db, participation)