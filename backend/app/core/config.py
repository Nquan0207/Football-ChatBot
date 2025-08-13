# app/core/config.py
from typing import List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Chatbot API"

    # CORS
    ALLOWED_HOSTS: List[str] = Field(default=["http://localhost:3000"])

    # MongoDB (used for everything: chat history, users, RAG, sessions, etc.)
    MONGO_URI: str = Field(default="mongodb://localhost:27017", env="MONGO_URI")
    MONGO_DB: str = Field(default="chatbot", env="MONGO_DB")

    # Gemini / LLM
    GEMINI_API_KEY: str = Field(default="", env="GEMINI_API_KEY")
    GEMINI_MODEL: str = Field(default="gemini-2.5-pro", env="GEMINI_MODEL")

    # RAG
    CHUNK_SIZE: int = Field(default=1000, env="CHUNK_SIZE")
    CHUNK_OVERLAP: int = Field(default=200, env="CHUNK_OVERLAP")
    VECTOR_DB_PATH: str = Field(default="./vector_db", env="VECTOR_DB_PATH")

    # Security / tokens
    SECRET_KEY: str = Field(
        default="ywg96hNzy6xSkEx-az9ivv07PuIzlQZ-YaR3dgh-HJo", env="SECRET_KEY"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # Logging
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")

    @field_validator("ALLOWED_HOSTS", mode="before")
    def split_hosts(cls, v):
        if isinstance(v, str):
            return [h.strip() for h in v.split(",") if h.strip()]
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
