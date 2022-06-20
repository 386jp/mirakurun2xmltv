from fastapi import APIRouter
router = APIRouter()

from app.routers import epg
router.include_router(epg.router, prefix="/epg", tags=["epg"])