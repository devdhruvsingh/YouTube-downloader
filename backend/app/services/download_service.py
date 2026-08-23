import uuid
from typing import Dict
import yt_dlp
from app.core.config import settings
from app.schemas.download import DownloadTaskResponse, DownloadStatus

# In-memory storage for tracking job statuses
download_jobs: Dict[str, DownloadTaskResponse] = {}


def init_download_job() -> str:
    """Generates a unique task ID and initializes job state."""
    task_id = str(uuid.uuid4())
    download_jobs[task_id] = DownloadTaskResponse(
        task_id=task_id,
        status=DownloadStatus.PENDING,
        progress_percentage=0.0,
    )
    return task_id


def process_download(task_id: str, url: str, format_id: str):
    """Executes the download in the background and updates job status."""
    if task_id not in download_jobs:
        return

    job = download_jobs[task_id]
    job.status = DownloadStatus.PROCESSING

    def progress_hook(d):
        if d["status"] == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 1
            downloaded = d.get("downloaded_bytes", 0)
            job.progress_percentage = round((downloaded / total) * 100, 2)
        elif d["status"] == "finished":
            job.progress_percentage = 100.0

    output_template = str(settings.DOWNLOAD_DIR / f"{task_id}_%(title)s.%(ext)s")

    ydl_opts = {
        "format": format_id,
        "outtmpl": output_template,
        "progress_hooks": [progress_hook],
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        job.status = DownloadStatus.COMPLETED
    except Exception as e:
        job.status = DownloadStatus.FAILED
        job.error_message = str(e)


def get_job_status(task_id: str) -> DownloadTaskResponse | None:
    """Retrieves the current status of a download job."""
    return download_jobs.get(task_id)