from sqlalchemy.orm import Session
from app.db.models import Participation, Challenge, ChallengeOption


def create_participation(
    db: Session,
    participation: Participation,
    challenge: Challenge,
    option: ChallengeOption,
):
    # Snapshot del reto
    participation.challenge_title_at_time = challenge.title
    participation.challenge_description_at_time = challenge.description
    participation.challenge_price_at_time = challenge.price
    participation.challenge_icon_at_time = challenge.icon
    participation.challenge_image_url_at_time = getattr(challenge, "image_url", None)
    participation.challenge_currency_at_time = getattr(challenge, "currency", "EUR")

    # Snapshot de la etapa
    if getattr(challenge, "stage", None):
        participation.stage_id_at_time = challenge.stage.id
        participation.stage_name_at_time = challenge.stage.name
    else:
        participation.stage_id_at_time = None
        participation.stage_name_at_time = None

    # Snapshot de la opción
    participation.option_name_at_time = option.name
    participation.option_description_at_time = option.description

    db.add(participation)
    db.commit()
    db.refresh(participation)
    return participation