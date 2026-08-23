from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from fastapi.responses import FileResponse

from app.core.config import settings
from app.schemas.download import DownloadRequest, DownloadStatus, DownloadTaskResponse
from app.services.download_service import (
    get_job_status,
    init_download_job,
    process_download,
)

router = APIRouter()


@router.post("/", response_model=DownloadTaskResponse, status_code=status.HTTP_202_ACCEPTED)
def start_download(payload: DownloadRequest, background_tasks: BackgroundTasks):
    task_id = init_download_job()
    background_tasks.add_task(process_download, task_id, payload.url, payload.format_id)
    return get_job_status(task_id)


@router.get("/{task_id}/status", response_model=DownloadTaskResponse)
def check_download_status(task_id: str):
    job = get_job_status(task_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Download task not found.",
        )
    return job


@router.get("/{task_id}/file")
def get_downloaded_file(task_id: str):
    job = get_job_status(task_id)
    if not job or job.status != DownloadStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is not ready or task does not exist.",
        )

    if not job.file_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No filename recorded for this download task.",
        )

    file_path = settings.DOWNLOAD_DIR / job.file_name

    if not file_path.is_file():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Requested file does not exist on server storage.",
        )

    return FileResponse(
        path=file_path,
        filename=job.file_name,
        media_type="application/octet-stream",
    )