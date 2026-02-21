from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.db.models import Challenge, ChallengeOption, Participation, Warrior, Stage
from app.repositories.participation_repo import create_participation
from app.schemas.participation import ParticipationCreate
from datetime import datetime
import json


def _load_config(option: ChallengeOption) -> dict:
    if not option.config_json:
        return {}
    try:
        return json.loads(option.config_json)
    except Exception:
        return {}


def _require_prediction_dict(prediction):
    if prediction is None:
        return {}
    if not isinstance(prediction, dict):
        raise HTTPException(status_code=422, detail="prediction must be an object")
    return prediction


def create_new_participation(db: Session, participation_data: ParticipationCreate):
    '''
    # =========================
    # Validate challenge
    # =========================
    '''

    challenge = (
        db.query(Challenge)
        .filter(
            Challenge.id == participation_data.challenge_id,
            Challenge.is_active == True,
        )
        .first()
    )
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found or inactive")

    '''
    # =========================
    # Validate option
    # =========================
    '''

    option = (
        db.query(ChallengeOption)
        .filter(
            ChallengeOption.id == participation_data.option_id,
            ChallengeOption.challenge_id == challenge.id,
        )
        .first()
    )
    if not option:
        raise HTTPException(status_code=404, detail="Option does not belong to challenge")

    '''
    # =========================
    # Validate amount
    # =========================
    '''

    if participation_data.amount < challenge.price:
        raise HTTPException(status_code=422, detail="Amount is less than challenge price")

    prediction = _require_prediction_dict(participation_data.prediction)
    config = _load_config(option)

    subject_type = option.subject_type
    answer_type = option.answer_type

    '''
    # =========================
    # 1) SUBJECT VALIDATION
    # =========================
    '''

    # helper: validate warrior
    def _validate_warrior_id(warrior_id: str):
        w = db.query(Warrior).filter(Warrior.id == warrior_id).first()
        if not w:
            raise HTTPException(status_code=422, detail="Invalid warrior_id")

    # helper: validate stage
    def _validate_stage_id(stage_id: str):
        s = db.query(Stage).filter(Stage.id == stage_id).first()
        if not s:
            raise HTTPException(status_code=422, detail="Invalid stage_id")

    if subject_type == "team":
        # no subject fields required
        pass

    elif subject_type == "warrior":
        warrior_id = prediction.get("warrior_id")
        if not warrior_id or not isinstance(warrior_id, str):
            raise HTTPException(status_code=422, detail="warrior_id required")
        _validate_warrior_id(warrior_id)

    elif subject_type == "stage":
        stage_id = prediction.get("stage_id")
        if not stage_id or not isinstance(stage_id, str):
            raise HTTPException(status_code=422, detail="stage_id required")
        _validate_stage_id(stage_id)

    elif subject_type == "warrior_stage":
        warrior_id = prediction.get("warrior_id")
        stage_id = prediction.get("stage_id")
        if not warrior_id or not isinstance(warrior_id, str):
            raise HTTPException(status_code=422, detail="warrior_id required")
        if not stage_id or not isinstance(stage_id, str):
            raise HTTPException(status_code=422, detail="stage_id required")
        _validate_warrior_id(warrior_id)
        _validate_stage_id(stage_id)

    else:
        raise HTTPException(status_code=422, detail=f"Unsupported subject_type: {subject_type}")

    '''
    # =========================
    # 2) ANSWER VALIDATION
    # =========================
    '''

    if answer_type == "warrior_pick":
        selections = prediction.get("selections", [])
        if not isinstance(selections, list):
            raise HTTPException(status_code=422, detail="selections must be a list")

        if len(selections) != option.number_of_selections:
            raise HTTPException(status_code=422, detail="Invalid number of selections")

        # unique
        if len(set(selections)) != len(selections):
            raise HTTPException(status_code=422, detail="Duplicate selections are not allowed")

        # all warriors exist
        if selections:
            rows = db.query(Warrior.id).filter(Warrior.id.in_(selections)).all()
            if len(rows) != len(selections):
                raise HTTPException(status_code=422, detail="Invalid warrior selection")

    elif answer_type == "stage_choice":
        # stage_choice is about choosing a stage as the answer.
        # If subject_type already requires stage_id, we interpret stage_id as subject.
        # So the answer stage must come as answer_stage_id to avoid ambiguity.
        answer_stage_id = prediction.get("answer_stage_id") or prediction.get("stage_id")
        if not answer_stage_id or not isinstance(answer_stage_id, str):
            raise HTTPException(status_code=422, detail="stage_id required")
        _validate_stage_id(answer_stage_id)

        # fixed stage constraint (if configured)
        fixed = config.get("fixed_stage_id")
        if fixed and answer_stage_id != fixed:
            raise HTTPException(status_code=422, detail=f"stage_id must be {fixed}")

    elif answer_type == "number":
        value = prediction.get("value")
        if value is None or not isinstance(value, (int, float)):
            raise HTTPException(status_code=422, detail="Numeric value required")
        if value < 0:
            raise HTTPException(status_code=422, detail="Value must be >= 0")

        # Optional: if warrior_stage number could be km within stage
        # and you want to constrain to 0..distance_km
        if subject_type == "warrior_stage" and config.get("number_is_km_within_stage"):
            stage_id = prediction.get("stage_id")
            stage = db.query(Stage).filter(Stage.id == stage_id).first()
            if stage and value > stage.distance_km:
                raise HTTPException(status_code=422, detail="Value exceeds stage distance")

    elif answer_type == "boolean":
        value = prediction.get("value")
        if not isinstance(value, bool):
            raise HTTPException(status_code=422, detail="Boolean value required")

    elif answer_type == "boolean_stage":
        value = prediction.get("value")
        if not isinstance(value, bool):
            raise HTTPException(status_code=422, detail="Boolean value required")

        # if true and requires stage: ensure stage_id present
        if value and config.get("stage_required_if_true", False):
            stage_id = prediction.get("stage_id")
            if not stage_id or not isinstance(stage_id, str):
                raise HTTPException(status_code=422, detail="stage_id required when true")
            _validate_stage_id(stage_id)

    elif answer_type == "boolean_stage_optional":
        value = prediction.get("value")
        if not isinstance(value, bool):
            raise HTTPException(status_code=422, detail="Boolean value required")

        stage_id = prediction.get("stage_id")
        if stage_id is not None:
            if not isinstance(stage_id, str) or not stage_id:
                raise HTTPException(status_code=422, detail="stage_id must be a string")
            _validate_stage_id(stage_id)

    elif answer_type == "time":
        value = prediction.get("value")
        if value is None or not isinstance(value, (int, float)):
            raise HTTPException(status_code=422, detail="Time value must be numeric (seconds)")
        if value <= 0:
            raise HTTPException(status_code=422, detail="Time value must be > 0")

        # Restricción opcional: fixed stage
        fixed = config.get("fixed_stage_id")
        if fixed:
            stage_id = prediction.get("stage_id")
            # si subject_type != warrior_stage, stage_id puede no venir; pero si viene, que sea el fijo
            if stage_id and stage_id != fixed:
                raise HTTPException(status_code=422, detail=f"stage_id must be {fixed}")

    elif answer_type == "text":
        value = prediction.get("value")
        if not isinstance(value, str) or not value.strip():
            raise HTTPException(status_code=422, detail="Text value required")

    elif answer_type == "choice":
        value = prediction.get("value")
        if not isinstance(value, str) or not value.strip():
            raise HTTPException(status_code=422, detail="Choice value required")
        allowed = config.get("allowed_values")
        if isinstance(allowed, list) and allowed:
            if value not in allowed:
                raise HTTPException(status_code=422, detail="Value not allowed")

    else:
        raise HTTPException(status_code=422, detail=f"Unsupported answer_type: {answer_type}")

    '''
    # =========================
    # Create participation
    # =========================
    '''

    new_participation = Participation(
        challenge_id=participation_data.challenge_id,
        option_id=participation_data.option_id,
        participant_name=participation_data.participant_name,
        email=participation_data.email,
        prediction_json=json.dumps(prediction, ensure_ascii=False),
        amount=participation_data.amount,
        message=participation_data.message,
        created_at=datetime.utcnow(),
    )

    return create_participation(db, new_participation)