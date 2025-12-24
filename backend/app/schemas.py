from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    query: str
    session_id: Optional[int] = None

class ChatResponse(BaseModel):
    winner: str
    winner_response: str
    loser_response: str
    judge_reason: str
    confidence: float
    gemini_response: str
    openai_response: str
    session_id: int

class MessageHistory(BaseModel):
    id: int
    query: str
    winner: str
    confidence: float
    created_at: datetime