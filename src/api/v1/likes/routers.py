from fastapi import APIRouter

from .views import router as likes_router


router = APIRouter(tags=["LIKES"])
router.include_router(likes_router)
