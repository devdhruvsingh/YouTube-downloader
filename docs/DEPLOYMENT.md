# Deployment Documentation

## 1. Overview

The application consists of:

- React frontend
- FastAPI backend
- yt-dlp
- FFmpeg
- Temporary file storage

The frontend and backend are deployed separately.

---

## 2. Deployment Architecture

```text
User
 │
 ▼
Frontend
React / Vite
 │
 │ HTTPS
 ▼
Backend
FastAPI
 │
 ├── yt-dlp
 │
 ├── FFmpeg
 │
 └── Temporary Storage
