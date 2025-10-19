import os
from pydantic import BaseModel

class Settings(BaseModel):
    env: str = os.getenv("ENV", "dev")
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://ci_user:ci_pass@db:5432/ci_main")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY") or None

settings = Settings()
