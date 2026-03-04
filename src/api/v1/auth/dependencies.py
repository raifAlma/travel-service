from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_token_unit_of_work
from infrastructure.repositories.postgres.token import PostgreSQLTokenUnitOfWork

from usecase.token.create_token.implemation import PostgreSQLCreateTokenUseCase
from usecase.token.refresh_token.implemation import PostgreSQLRefreshTokenUseCase


def get_token_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLTokenUnitOfWork:
    return build_token_unit_of_work(session)

def create_token_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = get_token_unit_of_work(session)
    return  PostgreSQLCreateTokenUseCase(uow=uow)

def refresh_token_use_case(
        session: AsyncSession = Depends(get_async_session),
):
    uow = get_token_unit_of_work(session)
    return PostgreSQLRefreshTokenUseCase(uow=uow)



'''
def create_user_use_case(
    session: AsyncSession = Depends(get_async_session),
):
    uow = build_user_unit_of_work(session)
    return PostgreSQLCreateUserUseCase(uow=uow)
'''