# backend/app/core/bootstrap_admin.py
import asyncio
from datetime import datetime
import secrets
import logging

from app.db.models.auth_models import UserCreate, Role
from app.services.user_mongo_service import get_user_by_email, create_user
from app.core.config import settings
from app.core.db import db

logger = logging.getLogger(__name__)

async def ensure_admin():
    admin_email = getattr(settings, "ADMIN_EMAIL", None)
    admin_username = getattr(settings, "ADMIN_USERNAME", "superadmin")
    admin_password = getattr(settings, "ADMIN_PASSWORD", None)

    # debug log (chỉ dev)
    logger.debug("Admin bootstrap values", extra={
        "ADMIN_EMAIL": admin_email,
        "ADMIN_USERNAME": admin_username,
        "HAS_ADMIN_PASSWORD": bool(admin_password),
    })

    if not admin_email:
        logger.warning("ADMIN_EMAIL not set; skipping admin bootstrap.")
        return

    existing = await get_user_by_email(admin_email)
    if existing:
        # đảm bảo có role admin
        if Role.admin not in existing.roles:
            await db["users"].update_one(
                {"_id": __import__("bson").ObjectId(existing.id)},
                {
                    "$addToSet": {"roles": Role.admin.value},
                    "$set": {"updated_at": datetime.utcnow()}
                }
            )
            logger.info("Upgraded existing user to admin: %s", admin_email)
        else:
            logger.info("Admin user already exists: %s", admin_email)
        return

    # tạo admin mới
    if not admin_password:
        admin_password = secrets.token_urlsafe(12)
        logger.warning("ADMIN_PASSWORD not set; auto-generated one for admin (dev only): %s", admin_password)

    user_in = UserCreate(
        username=admin_username,
        email=admin_email,
        password=admin_password,
        favorite_sports=["football"],
        favorite_team="Manchester United",
        membership=Role.premium,
    )
    try:
        admin = await create_user(user_in, roles=[Role.admin])
        logger.info("Created admin user: %s", admin_email)
        # (tuỳ chọn) log token dev-only
        from app.services.user_mongo_service import create_access_token
        token = create_access_token(
            data={"user_id": admin.id, "roles": [Role.admin.value]}
        )
        logger.debug("Admin access token (dev only): %s", token)
    except Exception as e:
        logger.error("Failed to create admin user: %s", e)
