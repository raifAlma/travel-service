from fastapi import APIRouter

from .views import router as author_router


router = APIRouter(tags=["Users"])
router.include_router(author_router)
