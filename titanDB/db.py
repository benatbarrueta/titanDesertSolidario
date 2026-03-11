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


class Warrior(Base):
    __tablename__ = "warrior"

    id = Column(String(16), primary_key=True)
    dorsal = Column(Integer, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    photo_url = Column(String(500), nullable=True)
    raised_cache = Column(Float, default=0.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_warrior_dorsal", "dorsal"),
    )


class Stage(Base):
    __tablename__ = "stage"

    id = Column(String(16), primary_key=True)  # "stage-1" .. "stage-6"
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

    # Gestión admin
    is_published = Column(Boolean, default=False, nullable=False)
    is_open_for_contributions = Column(Boolean, default=False, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)

    visible_from = Column(DateTime, nullable=True)
    visible_until = Column(DateTime, nullable=True)

    sort_order = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_stage_edition_year", "edition_year"),
        Index("ix_stage_stage_number", "stage_number"),
        Index("ix_stage_published_open_archived", "is_published", "is_open_for_contributions", "is_archived"),
    )


class Challenge(Base):
    __tablename__ = "challenge"

    id = Column(String(100), primary_key=True)

    stage_id = Column(
        String(16),
        ForeignKey("stage.id", ondelete="SET NULL"),
        nullable=True,
    )

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)

    price = Column(Float, default=0.0, nullable=False)
    currency = Column(String(3), default="EUR", nullable=False)

    icon = Column(String(32), nullable=True)
    image_url = Column(String(500), nullable=True)

    is_active = Column(Boolean, default=True, nullable=False)
    is_published = Column(Boolean, default=False, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)

    available_from = Column(DateTime, nullable=True)
    available_until = Column(DateTime, nullable=True)

    sort_order = Column(Integer, default=0, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    stage = relationship("Stage")

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

    __table_args__ = (
        Index("ix_challenge_stage_id", "stage_id"),
        Index("ix_challenge_active_published_archived", "is_active", "is_published", "is_archived"),
        Index("ix_challenge_available_window", "available_from", "available_until"),
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

    subject_type = Column(String(32), default="team", nullable=False)
    answer_type = Column(String(64), default="warrior_pick", nullable=False)
    config_json = Column(Text, nullable=True)

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

    prediction_json = Column(Text, nullable=False)

    amount = Column(Float, nullable=False)
    message = Column(Text, nullable=True)

    # Snapshot histórico del reto
    challenge_title_at_time = Column(String(255), nullable=False)
    challenge_description_at_time = Column(Text, nullable=True)
    challenge_price_at_time = Column(Float, nullable=False)
    challenge_icon_at_time = Column(String(32), nullable=True)
    challenge_image_url_at_time = Column(String(500), nullable=True)
    challenge_currency_at_time = Column(String(3), default="EUR", nullable=False)

    # Snapshot histórico de la etapa
    stage_id_at_time = Column(String(16), nullable=True)
    stage_name_at_time = Column(String(255), nullable=True)

    # Snapshot histórico de la opción
    option_name_at_time = Column(String(255), nullable=True)
    option_description_at_time = Column(Text, nullable=True)

    # Pago
    payment_status = Column(String(32), default="paid", nullable=False)
    payment_provider = Column(String(64), nullable=True)
    provider_reference = Column(String(255), nullable=True)
    paid_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    challenge = relationship("Challenge", back_populates="participations")
    option = relationship("ChallengeOption")

    __table_args__ = (
        Index("ix_participation_challenge_id", "challenge_id"),
        Index("ix_participation_option_id", "option_id"),
        Index("ix_participation_created_at", "created_at"),
        Index("ix_participation_payment_status", "payment_status"),
        Index("ix_participation_stage_id_at_time", "stage_id_at_time"),
    )


class AdminUser(Base):
    __tablename__ = "admin_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)

    role = Column(String(50), default="admin", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(Integer, primary_key=True, autoincrement=True)

    admin_id = Column(
        Integer,
        ForeignKey("admin_user.id", ondelete="SET NULL"),
        nullable=True,
    )

    entity_type = Column(String(50), nullable=False)
    entity_id = Column(String(100), nullable=False)
    action = Column(String(50), nullable=False)

    old_values_json = Column(Text, nullable=True)
    new_values_json = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    admin = relationship("AdminUser")

    __table_args__ = (
        Index("ix_audit_log_entity", "entity_type", "entity_id"),
        Index("ix_audit_log_created_at", "created_at"),
    )


DB_PATH = os.environ.get("SQLITE_DB_PATH", "./data/titan_desert_solidario.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},
)

Base.metadata.create_all(engine)

print("Base de datos creada en:", DB_PATH)

if __name__ == "__main__":
    while True:
        time.sleep(3600)