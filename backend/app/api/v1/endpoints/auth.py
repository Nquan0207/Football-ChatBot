from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from jose import JWTError
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.db.models.auth_models import (
    UserCreate,
    UserLogin,
    Token,
    UserResponse,
    Role,
    TokenData,
)
from app.services.user_mongo_service import (
    authenticate_user,
    create_user,
    create_access_token,
    get_user_by_id,
    decode_token,
)

router = APIRouter(prefix="/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_active_user(token: str = Depends(oauth2_scheme)):
    try:
        token_data: TokenData = decode_token(token)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    if not token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    user = await get_user_by_id(token_data.user_id)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive or missing user",
        )
    return user


def require_roles(required_roles: List[Role]):
    async def role_checker(user=Depends(get_current_active_user)):
        user_role_values = [r.value for r in user.roles]
        if not any(r.value in user_role_values for r in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient privileges",
            )
        return user

    return role_checker


@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate):
    # Quyết định admin: dùng env var hoặc domain whitelist thay vì hardcode trực tiếp
    roles = [Role.user]
    admin_domain = getattr(settings, "ADMIN_EMAIL_DOMAIN", None)
    if admin_domain and user_in.email.endswith(f"@{admin_domain}"):
        roles = [Role.admin]
    try:
        user = await create_user(user_in, roles=roles)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        roles=user.roles,
        favorite_sports=user.favorite_sports,
        favorite_team=user.favorite_team,
        membership=user.membership,
        is_active=user.is_active,
        created_at=user.created_at,
    )


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin):
    user = await authenticate_user(login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    access_token = create_access_token(
        data={"user_id": user.id, "roles": [r.value for r in user.roles]},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(access_token=access_token)
