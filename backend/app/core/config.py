import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SQLITE_DB_PATH: str = os.getenv("SQLITE_DB_PATH", "../runtime/db/titan_desert_solidario.db")

settings = Settings()