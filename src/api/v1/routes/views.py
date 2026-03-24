from api.v1.routes.models import RouteListResponse
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from infrastructure.repositories.postgres.route.exception import (
    RouteNameIsNotUnique, UserNotAuthorize,)
from usecase.route.create_route.abstarct import AbstractCreateRouteUseCase
from usecase.route.delete_route.abstract import AbstractDeleteRouteUseCase
from usecase.route.get_by_filters.abstract import \
    AbstractGetByFiltersRouteUseCase
from usecase.route.get_detail_route.abstract import \
    AbstractGetDetailRouteUseCase
from usecase.route.get_route.abstract import AbstractGetRouteUseCase
from usecase.route.update_route.abstract import AbstractUpdateRouteUseCase

from ...pydantic.models import RouteFilters
from .dependencies import (create_route_use_case, delete_route_use_case,
                           get_detail_by_id, get_route_by_filters,
                           get_route_use_case, update_route_use_case,)
from .models import (RouteCreate, RouteDetailResponse, RouteListResponse,
                     RouteResponse, RouteUpdate,)


router = APIRouter(prefix="/routes")

security = HTTPBearer()


async def get_token_from_header():
    credentials: HTTPAuthorizationCredentials = Depends(security)
    if not credentials:
        raise HTTPException(status_code=401, detail="please authenticate")
    return credentials.credentials


@router.post("", response_model=RouteCreate, status_code=status.HTTP_201_CREATED)
async def create_route(
    payload: RouteCreate,
    usecase: AbstractCreateRouteUseCase = Depends(create_route_use_case),
) -> JSONResponse:
    try:
        route = await usecase.execute(payload)
    except RouteNameIsNotUnique as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except UserNotAuthorize as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    return JSONResponse(content=jsonable_encoder(route))


@router.get("/{id}", response_model=RouteResponse, status_code=status.HTTP_200_OK)
async def get_route_by_id(
    id: int,
    usecase: AbstractGetRouteUseCase = Depends(get_route_use_case),
) -> JSONResponse:
    try:
        route = await usecase.execute(id)
        return JSONResponse(content=jsonable_encoder(route))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get(
    "/{id}/detail", response_model=RouteDetailResponse, status_code=status.HTTP_200_OK
)
async def get_detail_by_id(
    id: int,
    usecase: AbstractGetDetailRouteUseCase = Depends(get_detail_by_id),
) -> JSONResponse:
    try:
        route = await usecase.execute(id)
        return route
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{id}/filters", response_model=RouteListResponse)
async def get_routes_by_filters(
    filters: RouteFilters = Depends(),  # FastAPI распарсит query-параметры в модель
    usecase: AbstractGetByFiltersRouteUseCase = Depends(get_route_by_filters),
) -> RouteListResponse:
    routes, total = await usecase.execute(filters)
    return RouteListResponse(items=routes, total=total)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(
    id: int,
    usecase: AbstractDeleteRouteUseCase = Depends(delete_route_use_case),
):
    await usecase.execute(id)
    return None


@router.put("/{id}", response_model=RouteUpdate, status_code=status.HTTP_200_OK)
async def update_route(
    id: int,
    payload: RouteUpdate,
    usecase: AbstractUpdateRouteUseCase = Depends(update_route_use_case),
):
    try:
        route = await usecase.execute(id, payload)
    except RouteNameIsNotUnique as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    return JSONResponse(content=jsonable_encoder(route))
