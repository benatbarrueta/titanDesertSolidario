from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import Participation

def get_total_raised_and_participations(db: Session):
    total_raised = db.query(func.sum(Participation.amount)).scalar() or 0
    total_participations = db.query(func.count(Participation.id)).scalar() or 0
    return total_raised, total_participations