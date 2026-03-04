from fastapi import Depends
from fastapi.openapi.utils import status_code_ranges
from sqlalchemy.ext.asyncio import AsyncSession, session

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_waypoint_unit_of_work

from infrastructure.repositories.postgres.waypoint.uow import PostgreSQLWaypointUnitOfWork
from usecase.wapoint.craeate_waypoint.abstract import AbstractCreateWaypointUseCase
from usecase.wapoint.craeate_waypoint.implemation  import PostgreSQLCreateWaypointUseCase

from usecase.wapoint.delete_waypoint.implemation import PostgreSQLDeleteWaypointUseCase
from usecase.wapoint.update_waypoint.abstract import AbstractUpdateWaypointUseCase
from usecase.wapoint.update_waypoint.implemation import PostgreSQLUpdateWaypointUseCase
from usecase.wapoint.get_waypoint.abstract import AbstractGetWaypointUseCase
from usecase.wapoint.get_waypoint.implemation import PostgreSQLGetRouteUseCase


def get_waypoint_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLWaypointUnitOfWork:
    return build_waypoint_unit_of_work(session)


async def create_waypoint_use_case(
        session: AsyncSession = Depends(get_async_session)
) -> AbstractCreateWaypointUseCase:
    uow = get_waypoint_unit_of_work(session)
    return PostgreSQLCreateWaypointUseCase (uow=uow)

async def delete_waypoint_use_case(
        session: AsyncSession = Depends(get_async_session)
):
    uow = get_waypoint_unit_of_work(session)
    return PostgreSQLDeleteWaypointUseCase(uow=uow)

async def update_waypoint_use_case(
        session: AsyncSession = Depends(get_async_session)
)->AbstractUpdateWaypointUseCase:
    uow = get_waypoint_unit_of_work(session)
    return PostgreSQLUpdateWaypointUseCase(uow=uow)

async def get_waypoint_use_case(
        session: AsyncSession = Depends(get_async_session)
)-> AbstractGetWaypointUseCase:
    uow = get_waypoint_unit_of_work(session)
    return PostgreSQLGetRouteUseCase(uow=uow)