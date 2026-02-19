from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: str              # anon/public key

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:5500", "http://127.0.0.1:5500"]

    # JWT
    JWT_SECRET: str                # long random string — keep secret!
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60 * 8   # 8 hours

    # Admin credentials (only you log in — no user table needed)
    ADMIN_USERNAME: str
    ADMIN_PASSWORD_HASH: str       # bcrypt hash — generated via /api/auth/hashpw

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
