from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging

from app.core.config import settings
from app.api.v1.api import api_router
from app.core.logging import setup_logging
from app.core.bootstrap_admin import ensure_admin  # chắc chắn file tồn tại

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Chatbot API",
    description="High-performance async chatbot with RAG capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
origins = settings.ALLOWED_HOSTS
if isinstance(origins, str):
    import json
    origins = json.loads(origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "Chatbot API is running"}

# Bootstrap admin on startup
@app.on_event("startup")
async def on_startup():
    try:
        await ensure_admin()
        logger.info("Admin bootstrap completed.")
    except Exception as e:
        logger.error("Admin bootstrap failed: %s", e)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
