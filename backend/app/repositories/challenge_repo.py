from sqlalchemy.orm import Session
from sqlalchemy import func
from app.db.models import Challenge, ChallengeOption

def get_all_challenges(db: Session):
    return db.query(
        Challenge.id,
        Challenge.title,
        Challenge.icon,
        Challenge.price.label("min_price"),
        func.count(ChallengeOption.id).label("options_count")
    ).join(ChallengeOption, Challenge.id == ChallengeOption.challenge_id, isouter=True).group_by(Challenge.id).all()

def get_challenge_by_id(db: Session, challenge_id: str):
    return db.query(Challenge).filter(Challenge.id == challenge_id).first()