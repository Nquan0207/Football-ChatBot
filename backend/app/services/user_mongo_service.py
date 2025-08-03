# backend/app/services/user_mongo_service.py
from datetime import datetime, timedelta
from typing import Optional, List
from bson import ObjectId
from passlib.context import CryptContext
from jose import jwt, JWTError

from app.db.models.auth_models import Role, UserCreate, UserInDB, TokenData
from app.core.config import Settings
from app.core.logging import logger
from app.core.db import db

settings = Settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def user_doc_to_model(doc: dict) -> UserInDB:
    return UserInDB(
        id=str(doc["_id"]),
        username=doc["username"],
        email=doc["email"],
        hashed_password=doc["hashed_password"],
        roles=[Role(r) for r in doc.get("roles", [])],
        favorite_sports=doc.get("favorite_sports", []),
        favorite_team=doc.get("favorite_team"),
        membership=Role(doc.get("membership", Role.free.value)),
        is_active=doc.get("is_active", True),
        created_at=doc.get("created_at"),
        updated_at=doc.get("updated_at"),
    )

async def get_user_by_email(email: str) -> Optional[UserInDB]:
    doc = await db["users"].find_one({"email": email.lower()})
    if not doc:
        return None
    return user_doc_to_model(doc)

async def get_user_by_id(user_id: str) -> Optional[UserInDB]:
    try:
        oid = ObjectId(user_id)
    except Exception:
        return None
    doc = await db["users"].find_one({"_id": oid})
    if not doc:
        return None
    return user_doc_to_model(doc)

async def create_user(user_in: UserCreate, roles: Optional[List[Role]] = None) -> UserInDB:
    existing = await db["users"].find_one({
        "$or": [
            {"email": user_in.email.lower()},
            {"username": user_in.username}
        ]
    })
    if existing:
        raise ValueError("Email or username already registered")
    now = datetime.utcnow()
    role_values = [r.value for r in (roles or [Role.user])]
    doc = {
        "username": user_in.username,
        "email": user_in.email.lower(),
        "hashed_password": hash_password(user_in.password),
        "roles": role_values,
        "favorite_sports": user_in.favorite_sports or [],
        "favorite_team": user_in.favorite_team,
        "membership": user_in.membership.value,
        "is_active": True,
        "created_at": now,
        "updated_at": now,
    }
    res = await db["users"].insert_one(doc)
    doc["_id"] = res.inserted_id
    return user_doc_to_model(doc)

async def authenticate_user(email: str, password: str) -> Optional[UserInDB]:
    user = await get_user_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return token

def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        roles = payload.get("roles", [])
        return TokenData(user_id=user_id, roles=[Role(r) for r in roles])
    except JWTError as e:
        logger.debug("JWT decode error: %s", e)
        raise
