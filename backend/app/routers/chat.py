from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.message import Message
from app.models.user import User
from app.models.session import Session
from app.services.embedding_service import search_similar
from app.services.llm_service import run_agent, SYSTEM_PROMPT

router = APIRouter()



class ChatRequest(BaseModel):
    email: str
    message: str
    session_id: int | None = None


class ChatResponse(BaseModel):
    response: str



@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        user = User(email=request.email)
        db.add(user)
        db.commit()
        db.refresh(user)


    if request.session_id:
        session = db.query(Session).filter(Session.id == request.session_id).first()
    else:
        session = Session(user_id=user.id)
        db.add(session)
        db.commit()
        db.refresh(session)


    user_msg = Message(
        session_id=session.id,
        role="user",
        content=request.message
    )
    db.add(user_msg)
    db.commit()


    session_messages = (
        db.query(Message)
        .filter(Message.session_id == session.id)
        .order_by(Message.id.desc())
        .limit(20)
        .all()
    )

    session_messages = list(reversed(session_messages))


    rag_context = search_similar(request.message)
    rag_text = "\n\n".join(rag_context)


    conversation = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": f"Relevant knowledge:\n{rag_text}"}
    ]

    for msg in session_messages:
        conversation.append({
            "role": msg.role,
            "content": msg.content
        })


    final_answer = run_agent(conversation)

 
    ai_msg = Message(
        session_id=session.id,
        role="assistant",
        content=final_answer
    )
    db.add(ai_msg)
    db.commit()

    return ChatResponse(response=final_answer)