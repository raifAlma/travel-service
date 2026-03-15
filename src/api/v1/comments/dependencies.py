from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, session

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.di.injection import build_comment_unit_of_work
from infrastructure.repositories.postgres.comment.uow import PostgreSQLCommentUnitOfWork
from usecase.comment.create_comment.abstarct import AbstractCreateCommentUseCase
from usecase.comment.create_comment.implemation import PostgreSQLCreateCommentUseCase
from usecase.comment.get_by_id.implemation import PostgreSQLGetCommentUseCase
from usecase.comment.get_by_id.abstract import AbstractGetCommentUseCase

def get_comment_unit_of_work(
    session: AsyncSession = Depends(get_async_session),
) -> PostgreSQLCommentUnitOfWork:
    return build_comment_unit_of_work(session)


async def create_comment_use_case(
        session: AsyncSession = Depends(get_async_session)
) -> AbstractCreateCommentUseCase:
    uow = get_comment_unit_of_work(session)
    return PostgreSQLCreateCommentUseCase (uow=uow)

async def get_comment_by_id_use_case(
        session: AsyncSession = Depends(get_async_session),
) -> AbstractGetCommentUseCase:
    uow = get_comment_unit_of_work(session)
    return PostgreSQLGetCommentUseCase(uow=uow)