from fastapi import APIRouter
from app.api.v1.routes import download

api_router = APIRouter()

# Yeh line ensure karegi ki sabhi download routes /api/v1/download/... par map ho jayein
api_router.include_router(download.router, prefix="/download", tags=["Download"])