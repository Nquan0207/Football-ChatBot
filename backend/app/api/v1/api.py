from fastapi import APIRouter
from app.api.v1.endpoints import chat, rag, health

from app.api.v1.endpoints.auth import router as auth_router

api_router = APIRouter()
api_router.include_router(auth_router)  # /api/v1/auth
api_router.include_router(chat.router, prefix="/chat")
api_router.include_router(rag.router, prefix="/rag")
api_router.include_router(health.router, prefix="/health")