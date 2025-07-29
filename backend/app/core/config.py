from pydantic import Field
from pydantic_settings import BaseSettings
from typing import List, Optional
import os


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Chatbot API"
    
    # CORS
    ALLOWED_HOSTS: List[str] = Field(default=["http://localhost:3000", "http://localhost:5173"])
    
    # Database
    DATABASE_URL: str = Field(default="postgresql://user:password@localhost/chatbot")
    
    # Redis
    REDIS_URL: str = Field(default="redis://localhost:6379")
    
    # Gemini Settings
    GEMINI_API_KEY: str = Field(default="")
    GEMINI_MODEL: str = Field(default="gemini-2.5-pro")
    # Security
    SECRET_KEY: str = Field(default="3fa5a6fac76d2ac07bee09650ad3b37dda48477c0b00cdfd8418e71566968d81")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # RAG Settings
    CHUNK_SIZE: int = Field(default=1000)
    CHUNK_OVERLAP: int = Field(default=200)
    VECTOR_DB_PATH: str = Field(default="./vector_db")
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings() 