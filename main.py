from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime

app = FastAPI()

DATABASE_URL = "sqlite:///./chat.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer)
    receiver_id = Column(Integer)
    message = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


Base.metadata.create_all(bind=engine)


class UserCreate(BaseModel):
    name: str
    email: str


class MessageCreate(BaseModel):
    sender_id: int
    receiver_id: int
    message: str


@app.post("/users")
def create_user(user: UserCreate):

    db = SessionLocal()

    new_user = User(name=user.name, email=user.email)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users")
def get_users():

    db = SessionLocal()

    return db.query(User).all()


@app.post("/messages")
def send_message(msg: MessageCreate):

    db = SessionLocal()

    new_message = Message(
        sender_id=msg.sender_id,
        receiver_id=msg.receiver_id,
        message=msg.message
    )

    db.add(new_message)
    db.commit()

    return {"message": "Message sent"}


@app.get("/messages/{user1}/{user2}")
def get_conversation(user1: int, user2: int):

    db = SessionLocal()

    messages = db.query(Message).filter(
        ((Message.sender_id == user1) & (Message.receiver_id == user2)) |
        ((Message.sender_id == user2) & (Message.receiver_id == user1))
    ).all()

    return messages