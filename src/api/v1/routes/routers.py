from fastapi import APIRouter

from .views import router as routes_router

router = APIRouter(tags=["Routes"])
router.include_router(routes_router)

#router.include_router(author_router)