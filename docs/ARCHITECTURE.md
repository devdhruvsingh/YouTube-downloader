# System Architecture

## 1. Architecture Overview

The YouTube Downloader follows a client-server architecture.

```text
┌─────────────────────┐
│       Browser       │
│   React Frontend    │
└──────────┬──────────┘
           │ HTTP/HTTPS
           ▼
┌─────────────────────┐
│      FastAPI        │
│       Backend       │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     ▼           ▼
┌──────────┐ ┌──────────────┐
│ Services │ │  Validation  │
└────┬─────┘ └──────────────┘
     │
     ▼
┌─────────────────────┐
│       yt-dlp        │
│   Media Processing  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       FFmpeg        │
│   When Required     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Temporary Storage   │
└─────────────────────┘
