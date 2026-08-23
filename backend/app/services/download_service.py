import uuid
from typing import Dict, Optional
import yt_dlp

from app.core.config import settings
from app.schemas.download import DownloadStatus, DownloadTaskResponse

# In-memory task tracker
jobs_db: Dict[str, DownloadTaskResponse] = {}


def init_download_job() -> str:
    task_id = str(uuid.uuid4())
    jobs_db[task_id] = DownloadTaskResponse(
        task_id=task_id,
        status=DownloadStatus.PENDING,
        progress_percentage=0.0,
    )
    return task_id


def get_job_status(task_id: str) -> Optional[DownloadTaskResponse]:
    return jobs_db.get(task_id)


def process_download(task_id: str, url: str, format_id: str) -> None:
    job = jobs_db.get(task_id)
    if not job:
        return

    job.status = DownloadStatus.PROCESSING

    def progress_hook(d: dict):
        if d.get("status") == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate") or 0
            downloaded = d.get("downloaded_bytes", 0)
            if total > 0:
                job.progress_percentage = round((downloaded / total) * 100, 2)
        elif d.get("status") == "finished":
            job.progress_percentage = 100.0

    ydl_opts = {
        # Select best combined MP4 or best available video+audio format
        "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "outtmpl": str(settings.DOWNLOAD_DIR / "%(title)s.%(ext)s"),
        "progress_hooks": [progress_hook],
        "quiet": True,
        "no_warnings": True,
        # Bypass YouTube client restrictions
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"],
            }
        },
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            job.file_name = settings.DOWNLOAD_DIR.joinpath(filename).name
            job.status = DownloadStatus.COMPLETED
            job.progress_percentage = 100.0
    except Exception as e:
        job.status = DownloadStatus.FAILED
        job.error_message = str(e)