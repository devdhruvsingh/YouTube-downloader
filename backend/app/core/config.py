import os
from pathlib import Path
from typing import List

try:
    # Pydantic v2 preferred location
    from pydantic_settings import BaseSettings
except ImportError:
    # Fallback for Pydantic v1
    from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "YouTube Downloader API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # CORS configuration for frontend clients
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ]

    # Directories
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DOWNLOAD_DIR: Path = BASE_DIR / "downloads"

    # Job & storage constraints
    MAX_FILE_SIZE_MB: int = 500
    TEMP_FILE_TTL_HOURS: int = 1

    class Config:
        env_file = ".env"
        case_sensitive = True


# Instantiate global settings
settings = Settings()

# Ensure the downloads output folder exists on startup
settings.DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)