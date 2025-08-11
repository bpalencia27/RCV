from __future__ import annotations
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    PROVIDER: str = "gemini"
    OPENAI_API_KEY: str | None = None
    GEMINI_API_KEY: str | None = None
    MODEL_NAME: str = "gpt-4o-mini"
    GEMINI_MODEL: str = "gemini-1.5-flash"
    FRONTEND_ORIGIN: str = "http://localhost:5173"
    BASE_API_URL: str = "http://localhost:8000"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
