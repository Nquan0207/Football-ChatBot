# backend/app/core/db.py
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import IndexModel, ASCENDING
from pymongo.errors import ServerSelectionTimeoutError

from .config import Settings
from .logging import logger

settings = Settings()

mongo_client: AsyncIOMotorClient | None = None
db = None

def init_mongo():
    global mongo_client, db
    mongo_client = AsyncIOMotorClient(
        settings.MONGO_URI,
        serverSelectionTimeoutMS=5000,
        uuidRepresentation="standard",
    )
    db = mongo_client[settings.MONGO_DB]
    try:
        mongo_client.admin.command("ping")
        logger.info("✅ Connected to MongoDB Atlas.") 
    except ServerSelectionTimeoutError as e:
        logger.error("❌ Cannot connect to MongoDB Atlas: %s", e)
        raise

    # Ensure indexes for users collection
    users = db["users"]
    users.create_indexes([
        IndexModel([("email", ASCENDING)], unique=True),
        IndexModel([("username", ASCENDING)], unique=True),
    ])

# initialize on import (you can also call this explicitly in main)
init_mongo()
