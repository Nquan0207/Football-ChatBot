from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ChatMessage(BaseModel):
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    session_id: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    use_rag: bool = Field(default=True)
    context: Optional[List[str]] = Field(default=None)


class ChatResponse(BaseModel):
    message: str
    session_id: str
    timestamp: datetime
    sources: Optional[List[str]] = Field(default=None)
    processing_time: Optional[float] = Field(default=None)


class ChatSession(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    created_at: datetime
    last_activity: datetime
    message_count: int = 0 