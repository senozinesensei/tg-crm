from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://tgcrm:tgcrm_secret@db:5432/tgcrm"
    SECRET_KEY: str = "change-me-to-a-random-64-character-string-in-production"
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 24
    ALGORITHM: str = "HS256"

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    class Config:
        env_file = ".env"


settings = Settings()
