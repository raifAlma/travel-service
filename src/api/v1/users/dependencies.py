from fastapi import Depends
from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_user_unit_of_work
from infrastructure.repositories.postgres.user import PostgreSQLUserUnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession
from usecase.user.create_user.implemation import PostgreSQLCreateUserUseCase
from usecase.user.delete_user.implemation import PostgreSQLDeleteUserUseCase
from usecase.user.get_user.implemation import PostgreSQLGetUserUseCase
from usecase.user.update_user.abstract import AbstractUpdateUserUseCase
from usecase.user.update_user.implemation import PostgreSQLUpdateUserUseCase


def get_user_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLUserUnitOfWork:
    return build_user_unit_of_work(session)


def create_user_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_user_unit_of_work(session)
    return PostgreSQLCreateUserUseCase(uow=uow)


def get_user_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_user_unit_of_work(session)
    return PostgreSQLGetUserUseCase(uow=uow)


def delete_user_use_case(session: AsyncSession = Depends(get_async_session)):
    uow = get_user_unit_of_work(session)
    return PostgreSQLDeleteUserUseCase(uow=uow)


def update_user_use_case(
    session: AsyncSession = Depends(get_async_session),
) -> AbstractUpdateUserUseCase:
    uow = get_user_unit_of_work(session)
    return PostgreSQLUpdateUserUseCase(uow=uow)
