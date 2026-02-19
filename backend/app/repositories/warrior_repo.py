from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import Warrior, Participation

def get_all_warriors(db: Session):
    return db.query(
        Warrior.id,
        Warrior.dorsal,
        Warrior.name,
        func.sum(Participation.amount).label("raised")
    ).join(Participation, Warrior.id == Participation.participant_name, isouter=True).group_by(Warrior.id).all()

def get_warrior_by_id(db: Session, warrior_id: str):
    return db.query(Warrior).filter(Warrior.id == warrior_id).first()