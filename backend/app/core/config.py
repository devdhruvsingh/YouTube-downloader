from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings



class Setting(BaseSettings):
    PROJECT_NAME : str =  "Youtube Downloader API"
    VERSION : str = "1.0.0"
    API_V1_STR : str = "/api/v1"


# permitted origins
    ALLOWED_ORIGINS: List[str] = [
        "https://localhost:3000",
        "https://localhost:5173",
        "https://127.0.0.1:5173"
    ]

# file storage paths and limits
    BASE_DIR : Path = PATH(__file__).resolve().parent.parent.parent
    DOWNLOAD_DIR: Path = BASE_DIR / "downloads"
    MAX_FIlE_SIZE_MB : int = 1024 # this is the max size for the file

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# taget dowload directory exists
settings.DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)



