from sqlalchemy import Column, Integer, String, Float, Text, DateTime, SmallInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from database import Base    #Base class created in database.py

class Transcript(Base):
    __tablename__ = "transcripts"
    id = Column(Integer, primary_key=True)
    ticker = Column(String(10))
    company_name = Column(String(255))
    quarter = Column(SmallInteger)
    year = Column(SmallInteger)
    raw_text = Column(Text)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

class Segment(Base):
    __tablename__ = "segments"
    id = Column(Integer, primary_key=True)
    transcript_id = Column(Integer)
    segment_index = Column(SmallInteger)
    speaker = Column(String(100))
    role = Column(String(50))
    text = Column(Text)
    topic_label = Column(String(255))
    sentiment_score = Column(Float)
    tone = Column(String(50))
    hedging_phrases = Column(JSONB, default=list)

class Analysis(Base):
    __tablename__ = "analyses"
    id = Column(Integer, primary_key=True)
    transcript_id = Column(Integer)
    overall_sentiment = Column(Float)
    summary = Column(Text)
    notable_moments = Column(JSONB, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())