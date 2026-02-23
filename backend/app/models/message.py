from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.sql.functions import session_user
from app.core.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    role = Column(String, index=True)  #user or assistant 
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())