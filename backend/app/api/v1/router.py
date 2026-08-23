from fastapi import APIRouter
from app.api.v1.routes import analyze, download, health

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["Health"])
api_router.include_router(analyze.router, prefix="/analyze", tags=["Analyze"])
api_router.include_router(download.router, prefix="/download", tags=["Download"])