from __future__ import annotations
from datetime import datetime
from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, EmailStr, ConfigDict,Field


class UserCreate(BaseModel):
    email: str
    password: str
    username: Optional[str] = None

class UserOutput(BaseModel):
    id: int
    email: str
    username: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ChatTurn(BaseModel):
    user: str
    bot: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    text: str
    user_id: Optional[str] = None
    history: Optional[List[ChatTurn]] = None


class ChatResponse(BaseModel):
    response: str
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class HistoryItem(BaseModel):
    id: int
    role: Literal["user", "assistant"]
    content: str
    timestamp : datetime

    model_config = ConfigDict(from_attributes=True)

class HistoryList(BaseModel):
    user_id: Optional[int] = None
    items: List[HistoryItem]
    total: Optional[int] = None

class HistoryAppend(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class SoulSettingsRequest(BaseModel):
    tone: Literal["formal", "casual", "funny", "direct", "gentle"] = "gentle"
    empathy_level: int = Field(5, ge=1, le=10)
    reasoning_depth: int = Field(7, ge=1, le=10)
    creativity_level: int = Field(5, ge=1, le=10)
    memory_aggressiveness: int = Field(5, ge=1, le=10)
    boundaries: str = "Respectful and supportive"

class SoulSettingsUpdate(SoulSettingsRequest):
    "Used for creating and updating soul settings"
    pass

class SoulSettingsResponse(SoulSettingsRequest):
    id: int
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)









   

    
