from fastapi import APIRouter
from app.api.v1.endpoints import chat, rag, health, db_health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(rag.router, prefix="/rag", tags=["rag"]) 
api_router.include_router(db_health.router, prefix="/internal", tags=["DB"])