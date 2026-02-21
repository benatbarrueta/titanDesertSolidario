from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Warrior(Base):
    __tablename__ = "warrior"
    id = Column(String, primary_key=True, index=True)
    dorsal = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    raised_cache = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

class Challenge(Base):
    __tablename__ = "challenge"
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Float, nullable=False)
    icon = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    options = relationship("ChallengeOption", back_populates="challenge")

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
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

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
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index("ix_stage_edition_year", "edition_year"),
        Index("ix_stage_stage_number", "stage_number"),
    )