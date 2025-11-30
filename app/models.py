from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, func
from sqlalchemy.orm import relationship
from app.database import Base

# --- User Model ---
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(254), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan", passive_deletes=True)
    soul_settings = relationship("SoulSettings", back_populates="user", uselist=False, cascade="all, delete-orphan", passive_deletes=True)


# --- ChatMessage Model ---
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    role = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    user = relationship("User", back_populates="messages")


# --- SoulSettings Model ---

class SoulSettings(Base):
    __tablename__ = "soul_settings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    empathy_level=Column(Integer, default=5)
    tone=Column(String, default="gentle")
    reasoning_depth=Column(Integer, default=5)
    memory_aggressiveness=Column(Integer, default=5)
    boundaries=Column(String(500), default="Respectful and supportive")
    creativity_level=Column(Integer, default=5)

    user = relationship("User", back_populates="soul_settings", uselist=False)







    




