from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=getattr(settings, "VERSION", "1.0.0"),
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Fetch allowed origins from settings or fall back to permissive default for local development
origins = getattr(
    settings,
    "ALLOWED_ORIGINS",
    ["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:5173", "*"],
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API v1 router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
def read_root():
    """Root status endpoint for basic server check."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health",
    }