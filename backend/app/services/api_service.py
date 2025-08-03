from google import genai
from google.genai import types
import os
import asyncio
import time
import logging
from typing import List

from app.core.config import settings
from app.models.chat import ChatMessage, MessageRole

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self):
        api_key = settings.effective_gemini_api_key
        # Tạo client: nếu dùng API key (Gemini Developer API)
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            # fallback: dùng env vars / Vertex AI credentials
            self.client = genai.Client()
        self.model = getattr(settings, "GEMINI_MODEL", "gemini-2.5-pro")

    async def generate_response(
        self,
        messages: List[ChatMessage],
        temperature: float = 0.2,
        max_tokens: int = 1000
    ) -> str:
        prompt_parts = []
        for msg in messages:
            role = msg.role.value.capitalize()
            prompt_parts.append(f"{role}: {msg.content}")
        prompt = "\n".join(prompt_parts)

        start = time.time()
        loop = asyncio.get_running_loop()

        def sync_call():
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                ),
            )
            return response.text

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
        max_tokens: int = 1000
    ) -> str:
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

        return await self.generate_response(messages, temperature, max_tokens)
