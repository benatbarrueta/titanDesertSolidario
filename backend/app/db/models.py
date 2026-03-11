from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    DateTime,
    Boolean,
    ForeignKey,
    Text,
    Index,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Warrior(Base):
    __tablename__ = "warrior"

    id = Column(String, primary_key=True, index=True)
    dorsal = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    raised_cache = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    photo_url = Column(String, nullable=True)


class Stage(Base):
    __tablename__ = "stage"

    id = Column(String(16), primary_key=True)
    edition_year = Column(Integer, nullable=False, default=2026)
    stage_number = Column(Integer, nullable=False)
    name = Column(String(255), nullable=False)

    start_location = Column(String(255), nullable=True)
    finish_location = Column(String(255), nullable=True)

    distance_km = Column(Float, nullable=False)
    elevation_gain_m = Column(Integer, nullable=True)

    is_loop = Column(Boolean, default=False, nullable=False)
    is_marathon_sector = Column(Boolean, default=False, nullable=False)
    has_navigation_sector = Column(Boolean, default=False, nullable=False)
    has_timed_challenge = Column(Boolean, default=False, nullable=False)

    notes = Column(Text, nullable=True)

    # NUEVOS CAMPOS ADMIN
    is_published = Column(Boolean, default=False, nullable=False)
    is_open_for_contributions = Column(Boolean, default=False, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)

    visible_from = Column(DateTime, nullable=True)
    visible_until = Column(DateTime, nullable=True)

    sort_order = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    challenges = relationship("Challenge", back_populates="stage")

    __table_args__ = (
        Index("ix_stage_edition_year", "edition_year"),
        Index("ix_stage_stage_number", "stage_number"),
        Index(
            "ix_stage_published_open_archived",
            "is_published",
            "is_open_for_contributions",
            "is_archived",
        ),
    )


class Challenge(Base):
    __tablename__ = "challenge"

    id = Column(String, primary_key=True, index=True)

    # NUEVO: relación opcional con etapa
    stage_id = Column(String(16), ForeignKey("stage.id"), nullable=True, index=True)

    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)

    icon = Column(String, nullable=False)

    # NUEVOS CAMPOS
    currency = Column(String(3), default="EUR", nullable=False)
    image_url = Column(String(500), nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)

    available_from = Column(DateTime, nullable=True)
    available_until = Column(DateTime, nullable=True)

    sort_order = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    stage = relationship("Stage", back_populates="challenges")

    options = relationship("ChallengeOption", back_populates="challenge")
    participations = relationship("Participation", back_populates="challenge")

    __table_args__ = (
        Index("ix_challenge_active", "is_active"),
        Index("ix_challenge_published_archived", "is_published", "is_archived"),
        Index("ix_challenge_available_window", "available_from", "available_until"),
    )


class ChallengeOption(Base):
    __tablename__ = "challenge_option"

    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(String, ForeignKey("challenge.id"), nullable=False)

    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    subject_type = Column(String(32), default="team", nullable=False)
    answer_type = Column(String(64), default="warrior_pick", nullable=False)
    config_json = Column(Text, nullable=True)
    number_of_selections = Column(Integer, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    challenge = relationship("Challenge", back_populates="options")
    participations = relationship("Participation", back_populates="option")

    __table_args__ = (
        Index("ix_challenge_option_challenge_id", "challenge_id"),
        Index("ix_challenge_option_subject_type", "subject_type"),
        Index("ix_challenge_option_answer_type", "answer_type"),
    )


class Participation(Base):
    __tablename__ = "participation"

    id = Column(Integer, primary_key=True, index=True)

    challenge_id = Column(String, ForeignKey("challenge.id"), nullable=False)
    option_id = Column(Integer, ForeignKey("challenge_option.id"), nullable=False)

    participant_name = Column(String, nullable=False)
    email = Column(String, nullable=True)

    prediction_json = Column(Text, nullable=False)
    amount = Column(Float, nullable=False)
    message = Column(Text, nullable=True)

    # SNAPSHOT DEL RETO EN EL MOMENTO DE LA PARTICIPACIÓN
    challenge_title_at_time = Column(String(255), nullable=False)
    challenge_description_at_time = Column(Text, nullable=True)
    challenge_price_at_time = Column(Float, nullable=False)
    challenge_icon_at_time = Column(String(32), nullable=True)
    challenge_image_url_at_time = Column(String(500), nullable=True)
    challenge_currency_at_time = Column(String(3), default="EUR", nullable=False)

    # SNAPSHOT DE ETAPA
    stage_id_at_time = Column(String(16), nullable=True)
    stage_name_at_time = Column(String(255), nullable=True)

    # SNAPSHOT DE OPCIÓN
    option_name_at_time = Column(String(255), nullable=True)
    option_description_at_time = Column(Text, nullable=True)

    # CAMPOS DE PAGO
    payment_status = Column(String(32), default="paid", nullable=False)
    payment_provider = Column(String(64), nullable=True)
    provider_reference = Column(String(255), nullable=True)
    paid_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    challenge = relationship("Challenge", back_populates="participations")
    option = relationship("ChallengeOption", back_populates="participations")

    __table_args__ = (
        Index("ix_participation_challenge_id", "challenge_id"),
        Index("ix_participation_option_id", "option_id"),
        Index("ix_participation_created_at", "created_at"),
        Index("ix_participation_payment_status", "payment_status"),
        Index("ix_participation_stage_id_at_time", "stage_id_at_time"),
    )

class StageResult(Base):
    __tablename__ = "stage_result"

    id = Column(Integer, primary_key=True, index=True)

    stage_id = Column(String(16), ForeignKey("stage.id"), nullable=False, index=True)
    warrior_id = Column(String, ForeignKey("warrior.id"), nullable=False, index=True)

    position = Column(Integer, nullable=True)
    time_seconds = Column(Integer, nullable=True)

    punctures = Column(Integer, default=0, nullable=False)
    mechanical_issues = Column(Integer, default=0, nullable=False)
    crashes = Column(Integer, default=0, nullable=False)

    did_finish = Column(Boolean, default=True, nullable=False)
    received_medical_help = Column(Boolean, default=False, nullable=False)

    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    stage = relationship("Stage")
    warrior = relationship("Warrior")

    __table_args__ = (
        Index("ix_stage_result_stage_warrior", "stage_id", "warrior_id"),
    )