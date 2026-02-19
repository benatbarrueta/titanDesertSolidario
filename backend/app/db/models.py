from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, ForeignKey, Text
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
    type = Column(String, nullable=False)
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