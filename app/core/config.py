from pydantic import BaseSettings
from typing import List

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5500"]
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 480
    ADMIN_USERNAME: str
    ADMIN_PASSWORD_HASH: str

    class Config:
        env_file = ".env"

settings = Settings()ы