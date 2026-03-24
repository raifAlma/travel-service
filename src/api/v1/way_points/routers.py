from fastapi import APIRouter

from .views import router as way_router


router = APIRouter(tags=["Waypoints"])
router.include_router(way_router)
