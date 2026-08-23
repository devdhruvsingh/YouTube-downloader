from typing import List, Optional
from pydantic import BaseModel, HttpUrl, field_validator
from app.utils.validators import is_valid_youtube_url

class VideoAnalyzeRequest(BaseModel):
    url : str

    @field_validator("url")
    @classmethod
    def validate_youtube_url(cls, value: str) -> str:
        value = value.strip()
        if not is_valid_youtube_url(value):
            raise ValueError("Invalid Youtube URL provided")
        return value

class FormatOption(BaseMode):
    format_id : str
    ext : str
    resolution: Optional[str] = "audio only"
    filesize_approx : Optional[int] = None
    has_video : bool
    has_audio : bool
    quality_label : str

class VideoInfoResponse(BaseModel):
    video_id : str
    title : str
    author : str
    duration : str
    thumbnail : HttpUrl
    description : Optional[str]= None
    formats : List[FormatOption]
