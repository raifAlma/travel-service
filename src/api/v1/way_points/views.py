from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from infrastructure.repositories.postgres.waypoint.exception import WaypointNameIsNotUnique, RouteNotFound

from usecase.wapoint.craeate_waypoint.abstract import AbstractCreateWaypointUseCase
from usecase.wapoint.delete_waypoint.abstract import AbstractDeleteWaypointUseCase
from usecase.wapoint.update_waypoint.abstract import AbstractUpdateWaypointUseCase
from usecase.wapoint.get_waypoint.abstract import AbstractGetWaypointUseCase

from .dependencies import create_waypoint_use_case, delete_waypoint_use_case, update_waypoint_use_case, get_waypoint_use_case
from .models import WaypointSchema, WaypointUpdate


router = APIRouter(prefix='/waypoints')

security = HTTPBearer()
async def get_token_from_header():
    credentials: HTTPAuthorizationCredentials = Depends(security)
    if not credentials:
        raise HTTPException(status_code=401, detail='please authenticate')
    return credentials.credentials




@router.post("", response_model=WaypointSchema, status_code=status.HTTP_201_CREATED)
async def create_waypoint(
    payload: WaypointSchema,
    usecase: AbstractCreateWaypointUseCase= Depends(create_waypoint_use_case),
) -> JSONResponse:
    try:
        waypoint = await usecase.execute(payload)
    except WaypointNameIsNotUnique as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except RouteNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return JSONResponse(content=jsonable_encoder(waypoint))

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_waypoint(
        id: int,
        usecase: AbstractDeleteWaypointUseCase = Depends(delete_waypoint_use_case),
):
        await usecase.execute(id)
        return None

@router.put("", response_model=WaypointUpdate, status_code=status.HTTP_200_OK)
async def update_waypoint(
        id: int,
        payload: WaypointUpdate,
        usecase: AbstractUpdateWaypointUseCase = Depends(update_waypoint_use_case),
):
    try:
        waypoint = await usecase.execute(id, payload)
    except WaypointNameIsNotUnique as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except RouteNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return JSONResponse(content=jsonable_encoder(waypoint))

@router.get("", response_model=WaypointSchema, status_code=status.HTTP_200_OK)
async def get_waypoint_by_id(
    id: int,
    usecase: AbstractGetWaypointUseCase = Depends(get_waypoint_use_case),
) -> JSONResponse:
    try:
        waypoint = await usecase.execute(id)
        return JSONResponse(content=jsonable_encoder(waypoint))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

