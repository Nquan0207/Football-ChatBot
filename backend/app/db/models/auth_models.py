# backend/app/db/models/auth_models.py
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class Role(str, Enum):
    admin = "admin"
    user = "user"
    coach = "coach"        # mở rộng nếu cần
    premium = "premium"
    free = "free"

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8)
    favorite_sports: Optional[List[str]] = []
    favorite_team: Optional[str] = None
    membership: Role = Role.free  # membership tier
    # role assignment (admin) phải xử lý riêng

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserInDB(BaseModel):
    id: str
    username: str
    email: EmailStr
    hashed_password: str
    roles: List[Role]
    favorite_sports: Optional[List[str]] = []
    favorite_team: Optional[str] = None
    membership: Role = Role.free
    is_active: bool = True
    created_at: datetime
    updated_at: datetime

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr
    roles: List[Role]
    favorite_sports: Optional[List[str]] = []
    favorite_team: Optional[str] = None
    membership: Role
    is_active: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None
    roles: List[Role] = []
