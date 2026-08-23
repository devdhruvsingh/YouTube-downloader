from enum import Enum
from typing import Optional
from pydantic import BaseModel, HttpUrl

class DownloadStatus(str, Enum):
    PENDIING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DownloadRequest(BaseModel):
    url : str
    format_id : str
    audio_only : bool = False


class DownloadTaskResponse(BaseModel):
    task_id : str
    status : DownloadStatus
    progress_precentage: float = 0.0
    error_message : Optional[str] = None
    