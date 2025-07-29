from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.models.chat import ChatRequest, ChatResponse, ChatMessage
from app.services.chat_service import ChatService
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


def get_chat_service() -> ChatService:
    return ChatService()


@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Send a message and get AI response"""
    try:
        response = await chat_service.process_message(request)
        return response
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail="Failed to process message")


@router.get("/history/{session_id}", response_model=List[ChatMessage])
async def get_conversation_history(
    session_id: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Get conversation history for a session"""
    try:
        history = await chat_service.get_conversation_history(session_id)
        return history
    except Exception as e:
        logger.error(f"Error getting conversation history: {e}")
        raise HTTPException(status_code=500, detail="Failed to get conversation history")


@router.delete("/history/{session_id}")
async def clear_conversation_history(
    session_id: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """Clear conversation history for a session"""
    try:
        success = await chat_service.clear_conversation_history(session_id)
        if success:
            return {"message": "Conversation history cleared successfully"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except Exception as e:
        logger.error(f"Error clearing conversation history: {e}")
        raise HTTPException(status_code=500, detail="Failed to clear conversation history") 