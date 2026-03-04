from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.repositories.postgres.route import PostgreSQLRouteRepository
#from infrastructure.database.postgresql.session import get_async_session
from infrastructure.repositories.postgres.route.exception import RouteNameIsNotUnique
from usecase.route.create_route.abstarct import AbstractCreateRouteUseCase

from usecase.route.create_route.implemation import PostgreSQLCreateRouteUseCase
from usecase.route.delete_route.abstract import AbstractDeleteRouteUseCase

from usecase.route.get_route.abstract import AbstractGetRouteUseCase
from usecase.route.update_route.abstract import AbstractUpdateRouteUseCase
from .dependencies import  create_route_use_case, get_route_use_case, update_route_use_case, delete_route_use_case
from .models import RouteResponse, RouteDetailResponse, RouteCreate, RouteUpdate


router = APIRouter(prefix='/routes')

security = HTTPBearer()
async def get_token_from_header():
    credentials: HTTPAuthorizationCredentials = Depends(security)
    if not credentials:
        raise HTTPException(status_code=401, detail='please authenticate')
    return credentials.credentials


@router.post("", response_model=RouteCreate, status_code=status.HTTP_201_CREATED)
async def create_route(
    payload: RouteCreate,
    #current_route=Depends(get_route_unit_of_work),
    usecase: AbstractCreateRouteUseCase = Depends(create_route_use_case),
) -> JSONResponse:
    try:
        route = await usecase.execute(payload)
    except RouteNameIsNotUnique as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return JSONResponse(content=jsonable_encoder(route))

@router.get("", response_model=RouteResponse, status_code=status.HTTP_200_OK)
async def get_route_by_id(
    id: int,
    usecase: AbstractGetRouteUseCase = Depends(get_route_use_case),
) -> JSONResponse:
    try:
        route = await usecase.execute(id)
        return JSONResponse(content=jsonable_encoder(route))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_route(
        id: int,
        usecase: AbstractDeleteRouteUseCase = Depends(delete_route_use_case),
):
        await usecase.execute(id)
        return None

@router.put("", response_model=RouteUpdate, status_code=status.HTTP_200_OK)
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
