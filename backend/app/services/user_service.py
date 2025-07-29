from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.user import UserCreate, UserUpdate, User
from app.db.models.user import UserModel
import logging

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(UserModel).filter(UserModel.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(UserModel).filter(UserModel.username == username).first()

    def create_user(self, user: UserCreate) -> User:
        """Create a new user"""
        db_user = UserModel(
            email=user.email,
            username=user.username,
            hashed_password=self.get_password_hash(user.password)
        )
        try:
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            logger.info(f"Created new user: {user.username}")
            return db_user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating user: {e}")
            raise

    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user"""
        user = self.get_user_by_username(username)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, username: str) -> str:
        """Create JWT access token"""
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": username, "exp": expire}
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    def update_user(self, username: str, user_update: UserUpdate) -> Optional[User]:
        """Update user details"""
        db_user = self.get_user_by_username(username)
        if not db_user:
            return None

        update_data = user_update.dict(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = self.get_password_hash(update_data.pop("password"))

        try:
            for field, value in update_data.items():
                setattr(db_user, field, value)
            self.db.commit()
            self.db.refresh(db_user)
            logger.info(f"Updated user: {username}")
            return db_user
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating user: {e}")
            raise

    def deactivate_user(self, username: str) -> bool:
        """Deactivate a user account"""
        db_user = self.get_user_by_username(username)
        if not db_user:
            return False

        try:
            db_user.is_active = False
            self.db.commit()
            logger.info(f"Deactivated user: {username}")
            return True
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error deactivating user: {e}")
            raise
