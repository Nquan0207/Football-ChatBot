# app/utils/db.py
import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import IndexModel, ASCENDING
from pymongo.errors import PyMongoError

from app.core.config import settings

logger = logging.getLogger(__name__)

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None

async def init_db() -> None:
    global _client, _db
    if _db is not None:
        return  # already initialized

    _client = AsyncIOMotorClient(
        settings.MONGO_URI,
        serverSelectionTimeoutMS=5000,
    )
    try:
        # ping to verify connection
        await _client.admin.command("ping")
        logger.info("Connected to MongoDB")
    except Exception:
        logger.exception("MongoDB ping failed during init")
        raise

    _db = _client[settings.MONGO_DB]

    # ensure index on chats.session_id
    try:
        index = IndexModel([("session_id", ASCENDING)], name="idx_session_id")
        await _db.get_collection("chats").create_indexes([index])
        logger.debug("Ensured index on 'chats'.session_id")
    except PyMongoError:
        logger.exception("Failed to create index on chats collection")

def get_db() -> AsyncIOMotorDatabase:
    if _db is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _db

def get_collection(name: str):
    return get_db()[name]

def close_db() -> None:
    global _client, _db
    if _client is not None:
        _client.close()
    _client = None
    _db = None
