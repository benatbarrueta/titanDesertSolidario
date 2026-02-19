from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import Challenge, ChallengeOption, Participation, Warrior
from app.repositories.participation_repo import create_participation
from app.schemas.participation import ParticipationCreate
from datetime import datetime
import json

def create_new_participation(db: Session, participation_data: ParticipationCreate):
    # Validate challenge exists and is active
    challenge = db.query(Challenge).filter(Challenge.id == participation_data.challenge_id, Challenge.is_active == True).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found or inactive")

    # Validate option belongs to challenge
    option = db.query(ChallengeOption).filter(ChallengeOption.id == participation_data.option_id, ChallengeOption.challenge_id == challenge.id).first()
    if not option:
        raise HTTPException(status_code=404, detail="Option does not belong to the challenge")

    # Validate amount
    if participation_data.amount < challenge.price:
        raise HTTPException(status_code=422, detail="Amount is less than the challenge price")

    # Validate selections
    selections = participation_data.prediction.get("selections", [])
    if len(selections) != option.number_of_selections:
        raise HTTPException(status_code=422, detail="Invalid number of selections")

    # Validate selections exist as warriors
    warriors = db.query(Warrior.id).filter(Warrior.id.in_(selections)).all()
    if len(warriors) != len(selections):
        raise HTTPException(status_code=422, detail="One or more selected warriors do not exist")

    # Create participation
    new_participation = Participation(
        challenge_id=participation_data.challenge_id,
        option_id=participation_data.option_id,
        participant_name=participation_data.participant_name,
        email=participation_data.email,
        prediction_json=json.dumps(participation_data.prediction, ensure_ascii=False),
        amount=participation_data.amount,
        message=participation_data.message,
        created_at=datetime.utcnow()
    )

    return create_participation(db, new_participation)