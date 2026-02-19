from sqlalchemy.orm import Session
from app.db.models import Participation

def create_participation(db: Session, participation: Participation):
    db.add(participation)
    db.commit()
    db.refresh(participation)
    return participation