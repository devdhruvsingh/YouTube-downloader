from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from app.schemas.download import DownloadRequest, DownloadTaskResponse
from app.services.download_service import (
    init_download_job,
    process_download,
    get_job_status,
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