import os
import logging
import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.api import api_router
from app.core.logging import setup_logging
from app.utils.db import init_db, close_db  # Mongo helpers

# Setup logging early
setup_logging()
logger = logging.getLogger(__name__)

# Lifespan handler replaces deprecated on_event
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_db()
        logger.info("MongoDB initialized")
        yield
    except Exception:
        logger.exception("Failed during startup")
        # re-raise so FastAPI fails fast if DB init failed
        raise
    finally:
        try:
            close_db()
            logger.info("MongoDB connection closed")
        except Exception:
            logger.exception("Error closing MongoDB connection")


app = FastAPI(
    title="Chatbot API",
    description="High-performance async chatbot with RAG capabilities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS middleware: normalize allowed origins
_allow_origins = settings.ALLOWED_HOSTS
if isinstance(_allow_origins, str):
    # allow comma-separated string in env if needed
    _allow_origins = [o.strip() for o in _allow_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allow_origins or ["*"],  # fallback to permissive in dev if empty
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Health check
@app.get("/health", summary="Basic liveness check")
async def health_check():
    return {"status": "healthy", "message": "Chatbot API is running"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info",
    )
