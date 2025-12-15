import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey123")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./pocketsoc.db")
    AGENT_SECRET_KEY: str = os.getenv("AGENT_SECRET_KEY", "agentsecretkey12345678901234567890")

    class Config:
        env_file = ".env"

settings = Settings()
