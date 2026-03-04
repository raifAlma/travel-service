
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_route_unit_of_work
from infrastructure.repositories.postgres.route import PostgreSQLRouteUnitOfWork

from usecase.route.create_route.implemation import PostgreSQLCreateRouteUseCase
from usecase.route.delete_route.implemation import PostgreSQLDeleteRouteUseCase
from usecase.route.update_route.implemation import PostgreSQLUpdateRouteUseCase
from usecase.route.get_route.implemation import PostgreSQLGetRouteUseCase




def get_route_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLRouteUnitOfWork:
    return build_route_unit_of_work(session)


def create_route_use_case(
    session: AsyncSession = Depends(get_async_session)
):
    uow = get_route_unit_of_work(session)
    return PostgreSQLCreateRouteUseCase(uow=uow)

def update_route_use_case(
        session: AsyncSession = Depends(get_async_session)
):
    uow = get_route_unit_of_work(session)
    return PostgreSQLUpdateRouteUseCase(uow=uow)

def delete_route_use_case(
        session: AsyncSession = Depends(get_async_session)
):
    uow = get_route_unit_of_work(session)
    return PostgreSQLDeleteRouteUseCase(uow=uow)

def get_route_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_route_unit_of_work(session)
    return PostgreSQLGetRouteUseCase(uow=uow)

