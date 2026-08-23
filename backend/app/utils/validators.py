import re
from urllib.parse import parse_qs, urlparse

YOUTUBE_URL_REGEX = re.compile(
    r"^(https?://)?(www\.)?(youtube\.com|youtu\.be)/(watch\?v=|embed/|v/|shorts/)?([a-zA-Z0-9_-]{11})"
)


def extract_video_id(url: str) -> str | None:
    """Extracts the 11-character YouTube video ID from supported URL patterns."""
    match = YOUTUBE_URL_REGEX.match(url)
    if not match:
        return None

    parsed_url = urlparse(url)
    if "youtube.com" in parsed_url.netloc:
        query_params = parse_qs(parsed_url.query)
        if "v" in query_params:
            return query_params["v"][0]

    return match.group(5)


def is_valid_youtube_url(url: str) -> bool:
    """Returns True if the input URL is a valid, extractable YouTube link."""
    return extract_video_id(url) is not None