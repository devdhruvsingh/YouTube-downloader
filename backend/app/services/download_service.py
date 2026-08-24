import os
import re
import uuid
import asyncio
import glob
from typing import Dict, Any, Optional
import yt_dlp

tasks_db: Dict[str, Dict[str, Any]] = {}

def clean_youtube_url(url: str) -> str:
    if not url:
        return ""
    if '&' in url:
        url = url.split('&')[0]
    return url.strip()

def strip_ansi_codes(text: str) -> str:
    ansi_regex = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_regex.sub('', text)

def extract_video_info(url: str) -> Dict[str, Any]:
    clean_url = clean_youtube_url(url)
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'no_color': True,
        'skip_download': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(clean_url, download=False)
            
            formats_list = []
            seen_resolutions = set()

            # Extract Unique Resolutions
            for f in info.get('formats', []):
                height = f.get('height')
                fid = f.get('format_id')
                vcodec = f.get('vcodec', 'none')

                if height and height not in seen_resolutions and vcodec != 'none':
                    seen_resolutions.add(height)
                    
                    # Standard MP4 Option
                    formats_list.append({
                        'format_id': f"{fid}+bestaudio/best",
                        'label': f"{height}p • MP4 (Video + Audio)",
                        'ext': 'mp4',
                        'height': height,
                        'category': 'video'
                    })
                    
                    # WebM Option
                    formats_list.append({
                        'format_id': f"webm_{fid}",
                        'raw_fid': fid,
                        'label': f"{height}p • WebM (High Quality)",
                        'ext': 'webm',
                        'height': height,
                        'category': 'webm'
                    })

            formats_list.sort(key=lambda x: x.get('height', 0), reverse=True)

            # Audio Formats
            formats_list.extend([
                {'format_id': 'audio_mp3', 'label': 'Audio Only • MP3 (192kbps)', 'ext': 'mp3', 'category': 'audio'},
                {'format_id': 'audio_m4a', 'label': 'Audio Only • M4A (AAC)', 'ext': 'm4a', 'category': 'audio'},
                {'format_id': 'audio_wav', 'label': 'Audio Only • WAV (Lossless)', 'ext': 'wav', 'category': 'audio'}
            ])

            return {
                'id': info.get('id'),
                'title': info.get('title'),
                'thumbnail': info.get('thumbnail'),
                'duration': info.get('duration'),
                'uploader': info.get('uploader'),
                'formats': formats_list
            }
    except Exception as e:
        raise Exception(strip_ansi_codes(str(e)))

def _progress_hook(d: dict, task_id: str):
    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate') or 1
        downloaded = d.get('downloaded_bytes', 0)
        percentage = round((downloaded / total) * 100, 1)
        
        tasks_db[task_id].update({
            'status': 'processing',
            'progress_percentage': percentage,
            'downloaded_bytes': downloaded,
            'total_bytes': total
        })

async def process_download(task_id: str, url: str, format_id: str = "best", download_dir: str = "downloads"):
    os.makedirs(download_dir, exist_ok=True)
    clean_url = clean_youtube_url(url)
    output_template = os.path.join(download_dir, f"{task_id}.%(ext)s")

    # Audio Processing Configs
    if format_id.startswith('audio_'):
        audio_codec = format_id.split('_')[1]
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'quiet': True,
            'no_color': True,
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': audio_codec,
                'preferredquality': '192',
            }],
            'progress_hooks': [lambda d: _progress_hook(d, task_id)],
        }
    # WebM Video Processing Configs
    elif format_id.startswith('webm_'):
        raw_fid = format_id.replace('webm_', '')
        ydl_opts = {
            'format': f"{raw_fid}+bestaudio/best",
            'outtmpl': output_template,
            'merge_output_format': 'webm',
            'quiet': True,
            'no_color': True,
            'noplaylist': True,
            'progress_hooks': [lambda d: _progress_hook(d, task_id)],
        }
    # Default MP4 Configs
    else:
        selected_fmt = format_id if format_id and format_id != 'best' else 'bestvideo+bestaudio/best'
        ydl_opts = {
            'format': selected_fmt,
            'outtmpl': output_template,
            'merge_output_format': 'mp4',
            'quiet': True,
            'no_color': True,
            'noplaylist': True,
            'postprocessor_args': ['-c:v', 'copy', '-c:a', 'aac'],
            'progress_hooks': [lambda d: _progress_hook(d, task_id)],
        }

    def _run_download():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([clean_url])

            matching_files = glob.glob(os.path.join(download_dir, f"{task_id}.*"))
            if matching_files:
                final_file = matching_files[0]
                tasks_db[task_id].update({
                    'status': 'completed',
                    'progress_percentage': 100.0,
                    'file_path': os.path.abspath(final_file)
                })
            else:
                tasks_db[task_id].update({
                    'status': 'failed',
                    'error': 'Downloaded file missing on disk.'
                })
        except Exception as e:
            err_msg = strip_ansi_codes(str(e))
            tasks_db[task_id].update({
                'status': 'failed',
                'error': err_msg
            })

    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _run_download)

def init_download_job(url: str, format_id: str = "best") -> str:
    task_id = str(uuid.uuid4())
    tasks_db[task_id] = {
        'task_id': task_id,
        'job_id': task_id,
        'status': 'queued',
        'progress_percentage': 0,
        'file_path': None,
        'error': None
    }
    return task_id

def get_job_status(job_id: str) -> Optional[Dict[str, Any]]:
    return tasks_db.get(job_id)

process_download_task = process_download
initiate_download = init_download_job
get_task_status = get_job_status