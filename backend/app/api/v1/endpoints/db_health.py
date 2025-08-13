# app/api/v1/endpoints/db_health.py
from fastapi import APIRouter, HTTPException
from app.utils.db import get_db

router = APIRouter()

@router.get("/db/health", summary="MongoDB health check")
async def db_health():
    try:
        db = get_db()
        # ping the server
        await db.command("ping")
        collections = await db.list_collection_names()
        return {
            "status": "ok",
            "ping": True,
            "collections": collections
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"MongoDB unreachable: {e}")
