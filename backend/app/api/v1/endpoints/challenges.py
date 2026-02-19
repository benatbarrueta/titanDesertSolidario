from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.repositories.challenge_repo import get_all_challenges, get_challenge_by_id
from app.schemas.challenge import ChallengeBase, ChallengeDetail

router = APIRouter()

@router.get("/", response_model=list[ChallengeBase])
def list_challenges(db: Session = Depends(get_db)):
    return get_all_challenges(db)

@router.get("/{id}", response_model=ChallengeDetail)
def get_challenge(id: str, db: Session = Depends(get_db)):
    challenge = get_challenge_by_id(db, id)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    return challenge