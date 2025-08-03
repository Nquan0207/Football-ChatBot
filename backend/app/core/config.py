from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List, Optional
from pydantic import ConfigDict  # Pydantic v2
from pathlib import Path

class Settings(BaseSettings):
    # API / project
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Chatbot API"

    # CORS
    ALLOWED_HOSTS: List[str] = Field(default=["http://localhost:3000", "http://localhost:5173"])

    # Mongo
    MONGO_URI: str
    MONGO_DB: str

    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379")

    # Gemini / backward compatibility
    GEMINI_API_KEY: Optional[str] = Field(default=None, env="GEMINI_API_KEY")
    GOOGLE_API_KEY: Optional[str] = Field(default=None, env="GOOGLE_API_KEY")
    GEMINI_MODEL: str = Field(default="gemini-2.5-pro", env="GEMINI_MODEL")

    # Security
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)

    # RAG
    CHUNK_SIZE: int = Field(default=1000)
    CHUNK_OVERLAP: int = Field(default=200)
    VECTOR_DB_PATH: str = Field(default="./vector_db")

    # Logging
    LOG_LEVEL: str = Field(default="INFO")


    model_config = ConfigDict(
        env_file=".env",  
        case_sensitive=True,
        extra="ignore",
    )

    # Admin bootstrap
    ADMIN_EMAIL: Optional[str] = None
    ADMIN_USERNAME: str = "superadmin"
    ADMIN_PASSWORD: Optional[str] = None

    @property
    def effective_gemini_api_key(self) -> str:
        return self.GEMINI_API_KEY or self.GOOGLE_API_KEY or ""

# singleton instance
settings = Settings()
