from fastapi import FastAPI
from app.routers.chat import router as chat_router
from app.core.database import engine, Base 

from app.models.user import User
from app.models.message import  Message
from app.models.session import Session

from app.services.embedding_service import load_knowledge

load_knowledge()

app = FastAPI(title="ArchLily API")
Base.metadata.create_all(bind=engine)
app.include_router(chat_router)


@app.get("/")
def root():
    return {"message": "ArchLily is running 🌸"}
