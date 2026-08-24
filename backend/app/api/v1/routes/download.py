import os
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from app.services.download_service import (
    extract_video_info,
    initiate_download,
    process_download_task,
    get_task_status
)

router = APIRouter()

class AnalyzeRequest(BaseModel):
    url: str

class DownloadRequest(BaseModel):
    url: str
    format_id: Optional[str] = "best"

@router.post("/analyze/")
async def analyze_video(payload: AnalyzeRequest):
    try:
        data = extract_video_info(payload.url)
        return {"success": True, "data": data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/process")
async def start_download(payload: DownloadRequest, background_tasks: BackgroundTasks):
    try:
        task_id = initiate_download(payload.url, payload.format_id)
        background_tasks.add_task(process_download_task, task_id, payload.url, payload.format_id)
        return {"success": True, "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status/{task_id}")
async def check_status(task_id: str):
    status = get_task_status(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"success": True, "data": status}

@router.get("/file/{task_id}")
async def get_downloaded_file(task_id: str):
    status = get_task_status(task_id)
    if not status or status.get("status") != "completed":
        raise HTTPException(status_code=404, detail="File not ready or task not found")
    
    file_path = status.get("file_path")
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File missing on server disk")
    
    return FileResponse(file_path, media_type='application/octet-stream', filename=os.path.basename(file_path))