from typing import Dict, Any, List
import yt_dlp
from app.schemas.video import FormatOption, VideoInfoResponse


def extract_video_info(url: str) -> VideoInfoResponse:
    """Fetches video metadata and available formats without downloading the media file."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    formats: List[FormatOption] = []
    
    for f in info.get("formats", []):
        # Filter for relevant video/audio streams
        has_video = f.get("vcodec") != "none"
        has_audio = f.get("acodec") != "none"
        
        quality = f.get("format_note") or f.get("resolution") or ("Audio" if not has_video else "Video")
        
        formats.append(
            FormatOption(
                format_id=f.get("format_id"),
                ext=f.get("ext", "mp4"),
                resolution=f.get("resolution") if has_video else "audio only",
                filesize_approx=f.get("filesize") or f.get("filesize_approx"),
                has_video=has_video,
                has_audio=has_audio,
                quality_label=str(quality),
            )
        )

    return VideoInfoResponse(
        video_id=info.get("id"),
        title=info.get("title", "Unknown Title"),
        author=info.get("uploader", "Unknown Channel"),
        duration=int(info.get("duration", 0)),
        thumbnail=info.get("thumbnail"),
        description=info.get("description"),
        formats=formats,
    )