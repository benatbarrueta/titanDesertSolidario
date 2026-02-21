# db.py
from __future__ import annotations

import os
import time
from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    Float,
    String,
    Text,
    Boolean,
    DateTime,
    ForeignKey,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# =========================
# Models
# =========================

class Warrior(Base):
    __tablename__ = "warrior"

    # En frontend los IDs son strings tipo "101"
    id = Column(String(16), primary_key=True)  # e.g. "101"
    dorsal = Column(Integer, unique=True, nullable=False)
    name = Column(String(255), nullable=False)

    # cache opcional
    raised_cache = Column(Float, default=0.0, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_warrior_dorsal", "dorsal"),
    )


class Stage(Base):
    """
    Etapas oficiales Titan Desert 2026.
    Usamos id estable stage-1..stage-6 para poder referenciar desde predicciones.
    """
    __tablename__ = "stage"

    id = Column(String(16), primary_key=True)  # "stage-1" .. "stage-6"
    edition_year = Column(Integer, nullable=False, default=2026)
    stage_number = Column(Integer, nullable=False)  # 1..6

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

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_stage_edition_year", "edition_year"),
        Index("ix_stage_stage_number", "stage_number"),
    )


class Challenge(Base):
    __tablename__ = "challenge"

    # slug, e.g. "orden-y-posicion"
    id = Column(String(100), primary_key=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    price = Column(Float, default=0.0, nullable=False)

    icon = Column(String(32), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    options = relationship(
        "ChallengeOption",
        back_populates="challenge",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    participations = relationship(
        "Participation",
        back_populates="challenge",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )


class ChallengeOption(Base):
    __tablename__ = "challenge_option"

    id = Column(Integer, primary_key=True, autoincrement=True)
    challenge_id = Column(
        String(100),
        ForeignKey("challenge.id", ondelete="CASCADE"),
        nullable=False,
    )

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # 🔥 NUEVO: qué “sujeto” tiene la predicción
    # team | warrior | stage | warrior_stage
    subject_type = Column(String(32), default="team", nullable=False)

    # 🔥 NUEVO: tipo de respuesta
    # warrior_pick | stage_choice | boolean | number | time | text | choice
    # boolean_stage | boolean_stage_optional
    answer_type = Column(String(64), default="warrior_pick", nullable=False)

    # 🔥 NUEVO: JSON (texto) para configuración adicional:
    # - allowed_values
    # - min/max
    # - fixed_stage_id (p.ej. stage-4)
    # - stage_required_if_true
    # etc.
    config_json = Column(Text, nullable=True)

    # Sigue siendo útil para warrior_pick (Top 3, etc.)
    number_of_selections = Column(Integer, default=1, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    challenge = relationship("Challenge", back_populates="options")

    __table_args__ = (
        Index("ix_challenge_option_challenge_id", "challenge_id"),
        Index("ix_challenge_option_subject_type", "subject_type"),
        Index("ix_challenge_option_answer_type", "answer_type"),
    )


class Participation(Base):
    __tablename__ = "participation"

    id = Column(Integer, primary_key=True, autoincrement=True)

    challenge_id = Column(
        String(100),
        ForeignKey("challenge.id", ondelete="CASCADE"),
        nullable=False,
    )
    option_id = Column(
        Integer,
        ForeignKey("challenge_option.id", ondelete="RESTRICT"),
        nullable=False,
    )

    participant_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)

    # JSON serializado:
    # {
    #   "subject": {"warrior_id":"101","stage_id":"stage-3"},
    #   "answer": {"km_within_stage":45}
    # }
    prediction_json = Column(Text, nullable=False)

    amount = Column(Float, nullable=False)
    message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    challenge = relationship("Challenge", back_populates="participations")
    option = relationship("ChallengeOption")

    __table_args__ = (
        Index("ix_participation_challenge_id", "challenge_id"),
        Index("ix_participation_option_id", "option_id"),
        Index("ix_participation_created_at", "created_at"),
    )


# =========================
# DB init
# =========================

DB_PATH = os.environ.get("SQLITE_DB_PATH", "./data/titan_desert_solidario.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
)

Base.metadata.create_all(engine)

print("Base de datos creada en:", DB_PATH)


# Mantener el contenedor corriendo
if __name__ == "__main__":
    while True:
        time.sleep(3600)