from fastapi import Depends
from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_like_unit_of_work
from infrastructure.repositories.postgres.Like import PostgreSQLLikeUnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession
from usecase.like.add_like.implemation import PostgreSQLAddLikeUseCase
from usecase.like.delete_like.implemation import PostgreSQLDeleteLikeUseCase


def get_route_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLLikeUnitOfWork:
    return build_like_unit_of_work(session)


def create_like_use_case(session: AsyncSession = Depends(get_async_session)):
    uow = get_route_unit_of_work(session)
    return PostgreSQLAddLikeUseCase(uow=uow)


def delete_like_use_case(session: AsyncSession = Depends(get_async_session)):
    uow = get_route_unit_of_work(session)
    return PostgreSQLDeleteLikeUseCase(uow=uow)
