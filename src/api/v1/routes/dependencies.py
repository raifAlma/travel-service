from fastapi import Depends
from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_route_unit_of_work
from infrastructure.repositories.postgres.route import \
    PostgreSQLRouteUnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession
from usecase.route.create_route.implemation import PostgreSQLCreateRouteUseCase
from usecase.route.delete_route.implemation import PostgreSQLDeleteRouteUseCase
from usecase.route.get_by_filters.implemation import \
    PostgreSQLGetByFiltersRouteUseCase
from usecase.route.get_detail_route.imlemation import \
    PostgreSQLGetDetailRouteUseCase
from usecase.route.get_route.implemation import PostgreSQLGetRouteUseCase
from usecase.route.update_route.implemation import PostgreSQLUpdateRouteUseCase


def get_route_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLRouteUnitOfWork:
    return build_route_unit_of_work(session)


def create_route_use_case(session: AsyncSession = Depends(get_async_session)):
    uow = get_route_unit_of_work(session)
    return PostgreSQLCreateRouteUseCase(uow=uow)


def update_route_use_case(session: AsyncSession = Depends(get_async_session)):
    uow = get_route_unit_of_work(session)
    return PostgreSQLUpdateRouteUseCase(uow=uow)


def delete_route_use_case(session: AsyncSession = Depends(get_async_session)):
    uow = get_route_unit_of_work(session)
    return PostgreSQLDeleteRouteUseCase(uow=uow)


def get_route_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_route_unit_of_work(session)
    return PostgreSQLGetRouteUseCase(uow=uow)


def get_detail_by_id(session: AsyncSession = Depends(get_async_session)):
    uow = get_route_unit_of_work(session)
    return PostgreSQLGetDetailRouteUseCase(uow=uow)


def get_route_by_filters(session: AsyncSession = Depends(get_async_session)):
    uow = get_route_unit_of_work(session)
    return PostgreSQLGetByFiltersRouteUseCase(uow=uow)
