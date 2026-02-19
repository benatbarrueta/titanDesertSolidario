from sqlalchemy.orm import Session
from app.repositories.warrior_repo import get_all_warriors
from app.db.models import Participation
from app.schemas.warrior import WarriorOut
import json

def get_warriors_with_raised(db: Session):
    warriors = get_all_warriors(db)
    warrior_raised = {}

    participations = db.query(Participation).all()
    for participation in participations:
        prediction = json.loads(participation.prediction_json)
        selections = prediction.get("selections", [])
        amount_per_warrior = participation.amount / len(selections)

        for warrior_id in selections:
            if warrior_id not in warrior_raised:
                warrior_raised[warrior_id] = 0
            warrior_raised[warrior_id] += amount_per_warrior

    result = []
    for warrior in warriors:
        result.append(WarriorOut(
            id=warrior.id,
            dorsal=warrior.dorsal,
            name=warrior.name,
            raised=warrior_raised.get(warrior.id, 0.0)
        ))

    return result