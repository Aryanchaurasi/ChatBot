from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import ChatRequest, ChatResponse
from ..models import ChatSession, Message
from ..services.llm_service import get_best_response

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Get or create session
        if request.session_id:
            session = db.query(ChatSession).filter(ChatSession.id == request.session_id).first()
            if not session:
                session = ChatSession()
                db.add(session)
                db.commit()
                db.refresh(session)
        else:
            session = ChatSession()
            db.add(session)
            db.commit()
            db.refresh(session)
        
        # Get LLM responses
        result = await get_best_response(request.query)
        
        # Save to database
        message = Message(
            session_id=session.id,
            query=request.query,
            gemini_response=result["gemini_response"],
            openai_response=result["openai_response"],
            winner=result["winner"],
            judge_reason=result["judge_reason"],
            confidence=result["confidence"]
        )
        db.add(message)
        db.commit()
        
        return ChatResponse(
            winner=result["winner"],
            winner_response=result["winner_response"],
            loser_response=result["loser_response"],
            judge_reason=result["judge_reason"],
            confidence=result["confidence"],
            gemini_response=result["gemini_response"],
            openai_response=result["openai_response"],
            session_id=session.id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history/{session_id}")
async def get_history(session_id: int, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.session_id == session_id).order_by(Message.created_at.desc()).limit(50).all()
    return messages