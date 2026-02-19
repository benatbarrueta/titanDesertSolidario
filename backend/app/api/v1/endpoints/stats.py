from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.stats_service import get_stats
from app.schemas.stats import StatsResponse

router = APIRouter()

@router.get("/", response_model=StatsResponse)
def get_statistics(db: Session = Depends(get_db)):
    return get_stats(db)