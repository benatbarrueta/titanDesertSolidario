from sqlalchemy.orm import Session
from app.repositories.stats_repo import get_total_raised_and_participations
from app.schemas.stats import StatsResponse

def get_stats(db: Session) -> StatsResponse:
    total_raised, total_participations = get_total_raised_and_participations(db)
    return StatsResponse(
        total_raised=total_raised,
        total_participations=total_participations,
        currency="EUR"
    )