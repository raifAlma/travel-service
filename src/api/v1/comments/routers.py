from fastapi import APIRouter

from .views import router as comment_router


router = APIRouter(tags=["Comments"])
router.include_router(comment_router)
