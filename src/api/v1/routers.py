from api.v1.auth import routers as auth_router
from api.v1.comments import routers as comments_router
from api.v1.likes import routers as likes_router
from api.v1.routes import routers as routes_router
from api.v1.users import routers as author_router
from api.v1.way_points import routers as waypoints_router
from fastapi import APIRouter


# router = FastAPI(version="1.0")
router = APIRouter(prefix="/api/v1")

router.include_router(author_router.router)
router.include_router(auth_router.router)
router.include_router(routes_router.router)
router.include_router(waypoints_router.router)
router.include_router(likes_router.router)
router.include_router(comments_router.router)
