import asyncio
import time
import uuid
from typing import List, Optional
from datetime import datetime
from app.models.chat import ChatMessage, ChatResponse, MessageRole, ChatRequest
from app.services.api_service import GeminiService
from app.services.rag_service import RAGService
import logging

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        self.ai_service = GeminiService()
        self.rag_service = RAGService()
        self.conversation_history = {}  # In production, use Redis or database
    
    async def process_message(self, request: ChatRequest) -> ChatResponse:
        """Process a chat message and generate response"""
        try:
            start_time = time.time()
            
            # Generate or get session ID
            session_id = request.session_id or str(uuid.uuid4())
            
            # Get context if RAG is enabled
            context = []
            if request.use_rag:
                context = await self.rag_service.get_context_for_query(request.message)
            
            # Get conversation history for the session
            history = self.conversation_history.get(session_id, [])
            
            # Generate response
            if context and request.use_rag:
                response_text = await self.ai_service.generate_response_with_context(
                    request.message, context
                )
            else:
                # Add current message to history
                messages = history + [
                    ChatMessage(role=MessageRole.USER, content=request.message)
                ]
                response_text = await self.ai_service.generate_response(messages)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Store in conversation history (simplified - use database in production)
            if session_id not in self.conversation_history:
                self.conversation_history[session_id] = []
            
            self.conversation_history[session_id].extend([
                ChatMessage(role=MessageRole.USER, content=request.message),
                ChatMessage(role=MessageRole.ASSISTANT, content=response_text)
            ])
            
            # Create response
            response = ChatResponse(
                message=response_text,
                session_id=session_id,
                timestamp=datetime.utcnow(),
                sources=context if context else None,
                processing_time=processing_time
            )
            
            logger.info(f"Processed message in {processing_time:.2f}s")
            return response
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            raise
    
    async def get_conversation_history(self, session_id: str) -> List[ChatMessage]:
        """Get conversation history for a session"""
        try:
            return self.conversation_history.get(session_id, [])
        except Exception as e:
            logger.error(f"Error getting conversation history: {e}")
            return []
    
    async def clear_conversation_history(self, session_id: str) -> bool:
        """Clear conversation history for a session"""
        try:
            if session_id in self.conversation_history:
                del self.conversation_history[session_id]
                return True
            return False
        except Exception as e:
            logger.error(f"Error clearing conversation history: {e}")
            return False
    
    async def add_documents_to_rag(self, file_paths: List[str]) -> bool:
        """Add documents to RAG system"""
        try:
            return await self.rag_service.add_documents(file_paths)
        except Exception as e:
            logger.error(f"Error adding documents to RAG: {e}")
            return False
    
    def get_rag_stats(self) -> dict:
        """Get RAG system statistics"""
        try:
            return self.rag_service.get_database_stats()
        except Exception as e:
            logger.error(f"Error getting RAG stats: {e}")
            return {"total_documents": 0, "status": "error"} 