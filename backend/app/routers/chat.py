from fastapi import APIRouter, Depends
from openai import conversations
from openai.resources.chat import Chat
from openai.types.responses import response
from pydantic import BaseModel
from app.services.llm_service import generate_response, SYSTEM_PROMPT
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.message import Message
from app.models.user import User
from app.models.session import Session

router = APIRouter()


class ChatRequest(BaseModel):
    email: str
    message: str
    session_id: int | None = None


class ChatResponse(BaseModel):
    response: str


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):

    # get or create user
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        user = User(email=request.email)
        db.add(user)
        db.commit()
        db.refresh(user)

    # create session id if not provided
    if request.session_id:
        session = db.query(Session).filter(Session.id == request.session_id).first()
    else:
        session = Session(user_id=user.id)
        db.add(session)
        db.commit()
        db.refresh(session)

    # save user message
    user_msg = Message(session_id=session.id, role="user", content=request.message)
    db.add(user_msg)
    db.commit()

    # fetch ALL previous
    all_messages = db.query(Message).order_by(Message.id).all()

    # Fetch session message only
    session_message = (
        db.query(Message)
        .filter(Message.session_id == session.id)
        .order_by(Message.id.desc())
        .limit(20)
        .all()
    )

    #reverse because we fetched desc
    session_message = list(reversed(session_message))

    # convert to openAI format
    conversations = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in session_message:
        conversations.append({"role": msg.role, "content": msg.content})

    # Generate AI response
    reply = generate_response(conversations)

    # Save assistant response
    ai_msg = Message(session_id=session.id, role="assistant", content=reply)
    db.add(ai_msg)
    db.commit()

    return ChatResponse(response=reply)
