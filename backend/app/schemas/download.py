from enum import Enum
from typing import Optional
from pydantic import BaseModel


class DownloadStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DownloadRequest(BaseModel):
    url: str
    format_id: str


class DownloadTaskResponse(BaseModel):
    task_id: str
    status: DownloadStatus
    progress_percentage: float = 0.0
    error_message: Optional[str] = None
    file_name: Optional[str] = None