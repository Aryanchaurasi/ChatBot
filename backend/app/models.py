from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ChatSession(Base):
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, index=True)
    query = Column(Text)
    gemini_response = Column(Text)
    openai_response = Column(Text)
    winner = Column(String(10))
    judge_reason = Column(Text)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)