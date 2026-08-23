from fastapi import APIRouter, HTTPException, status
from app.schemas.video import VideoAnalyzeRequest, VideoInfoResponse
from app.services.youtube_service import extract_video_info

router = APIRouter()


@router.post("/", response_model=VideoInfoResponse, status_code=status.HTTP_200_OK)
def analyze_video(payload: VideoAnalyzeRequest):
    try:
        return extract_video_info(payload.url)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to analyze video: {str(e)}",
        )