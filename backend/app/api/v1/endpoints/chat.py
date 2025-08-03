from fastapi import APIRouter, HTTPException, Depends
from typing import List
import logging

from app.models.chat import ChatRequest, ChatResponse, ChatMessage
from app.services.chat_service import ChatService
from app.api.v1.endpoints.auth import get_current_active_user, require_roles
from app.db.models.auth_models import Role, UserInDB

logger = logging.getLogger(__name__)
router = APIRouter()

# reuse single shared service instance (can later be replaced by DI if needed)
chat_service = ChatService()

@router.post("/message", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    current_user: UserInDB = Depends(get_current_active_user),
):
    """Send a message and get AI response"""
    try:
        response = await chat_service.process_message(request)
        return response
    except Exception as e:
        logger.exception("Error processing message")
        raise HTTPException(status_code=500, detail="Failed to process message")


@router.get("/history/{session_id}", response_model=List[ChatMessage])
async def get_conversation_history(
    session_id: str,
    current_user: UserInDB = Depends(get_current_active_user),
):
    """Get conversation history for a session"""
    try:
        history = await chat_service.get_conversation_history(session_id)
        if history is None:
            raise HTTPException(status_code=404, detail="Session not found")
        return history
    except Exception as e:
        logger.exception("Error getting conversation history")
        raise HTTPException(status_code=500, detail="Failed to get conversation history")


@router.delete("/history/{session_id}")
async def clear_conversation_history(
    session_id: str,
    current_user: UserInDB = Depends(get_current_active_user),
):
    """Clear conversation history for a session"""
    try:
        success = await chat_service.clear_conversation_history(session_id)
        if success:
            return {"message": "Conversation history cleared successfully"}
        else:
            raise HTTPException(status_code=404, detail="Session not found")
    except Exception as e:
        logger.exception("Error clearing conversation history")
        raise HTTPException(status_code=500, detail="Failed to clear conversation history")


# example admin-only endpoint
@router.get("/admin-info")
async def admin_info(user: UserInDB = Depends(require_roles([Role.admin]))):
    return {"msg": f"Hello admin {user.username}"}
