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
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# =========================
# Models
# =========================

class Warrior(Base):
    __tablename__ = "warrior"

    # En frontend los IDs son strings tipo "101", pero en DB lo guardamos como string estable
    id = Column(String(16), primary_key=True)  # e.g. "101"
    dorsal = Column(Integer, unique=True, nullable=False)  # 101..125
    name = Column(String(255), nullable=False)

    # Si no quieres cache, puedes eliminar esta columna y calcularlo por agregación
    raised_cache = Column(Float, default=0.0, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_warrior_dorsal", "dorsal"),
    )


class Challenge(Base):
    __tablename__ = "challenge"

    # slug, e.g. "orden-y-posicion"
    id = Column(String(100), primary_key=True)

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    # precio mínimo
    price = Column(Float, default=0.0, nullable=False)

    icon = Column(String(32), nullable=True)  # emoji o nombre
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

    # Por ahora: "ranking"
    type = Column(String(50), default="ranking", nullable=False)

    # cuántos corredores puede seleccionar el usuario
    number_of_selections = Column(Integer, default=1, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    challenge = relationship("Challenge", back_populates="options")

    __table_args__ = (
        Index("ix_challenge_option_challenge_id", "challenge_id"),
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

    # JSON serializado (p.ej. {"type":"ranking","selections":["101","108","125"]})
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
    connect_args={"check_same_thread": False},  # útil para FastAPI
)

Base.metadata.create_all(engine)

print("Base de datos creada en:", DB_PATH)


# Mantener el contenedor corriendo (misma idea que tu ejemplo)
if __name__ == "__main__":
    while True:
        time.sleep(3600)
