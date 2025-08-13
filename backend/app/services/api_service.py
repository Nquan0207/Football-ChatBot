import asyncio
import time
from typing import List
import logging

import google.generativeai as genai

from app.core.config import settings
from app.models.chat import ChatMessage, MessageRole

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        # Cấu hình SDK
        if settings.GOOGLE_API_KEY:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
        else:
            # nếu dùng credential file, đặt GOOGLE_APPLICATION_CREDENTIALS env var
            genai.configure()

        # model có thể là "gemini-flash" hoặc "gemini-pro"
        self.model = getattr(settings, "GEMINI_MODEL", "gemini-2.5-pro")

    async def generate_response(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.2,
    ) -> str:
        """Generate response using Google Gemini Flash via threadpool"""
        # Chuẩn bị payload cho Gemini
        genai_messages = [
            {"author": msg.role.value, "content": msg.content}
            for msg in messages
        ]

        start = time.time()
        loop = asyncio.get_running_loop()

        def sync_call():
            resp = genai.chat.completions.create(
                model=self.model,
                messages=genai_messages,
                temperature=temperature,
            )
            return resp.candidates[0].content

        try:
            answer = await loop.run_in_executor(None, sync_call)
            elapsed = time.time() - start
            logger.info(f"Gemini response generated in {elapsed:.2f}s")
            return answer

        except Exception as e:
            logger.error(f"Error generating Gemini response: {e}")
            raise

    async def generate_response_with_context(
        self,
        user_message: str,
        context: List[str],
        temperature: float = 0.2,
    ) -> str:
        """Generate response with RAG context via Gemini"""
        # Tạo system message
        context_text = "\n".join(context)
        system_content = (
            "You are a helpful AI assistant. Use the following context to answer the user's question:\n\n"
            f"{context_text}\n\n"
            "If the context doesn't contain relevant information, please say so politely."
        )

        messages = [
            ChatMessage(role=MessageRole.SYSTEM, content=system_content),
            ChatMessage(role=MessageRole.USER, content=user_message)
        ]

        return await self.generate_response(messages, temperature)
