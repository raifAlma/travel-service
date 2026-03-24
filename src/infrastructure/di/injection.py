from container import Container
from infrastructure.repositories.postgres.comment.uow import \
    PostgreSQLCommentUnitOfWork
from infrastructure.repositories.postgres.Like.uow import \
    PostgreSQLLikeUnitOfWork
from infrastructure.repositories.postgres.route.uow import \
    PostgreSQLRouteUnitOfWork
from infrastructure.repositories.postgres.token.uow import \
    PostgreSQLTokenUnitOfWork
from infrastructure.repositories.postgres.user.uow import \
    PostgreSQLUserUnitOfWork
from infrastructure.repositories.postgres.waypoint.uow import \
    PostgreSQLWaypointUnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession


def build_user_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLUserUnitOfWork:
    return Container.user_uow_factory(session=session)


def build_token_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLTokenUnitOfWork:
    return Container.token_uow_factory(session=session)


def build_route_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLRouteUnitOfWork:
    return Container.route_uow_factory(session=session)


def build_waypoint_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLWaypointUnitOfWork:
    return Container.waypoint_uow_factory(session=session)


def build_comment_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLCommentUnitOfWork:
    return Container.comment_uow_factory(session=session)


def build_like_unit_of_work(
    session: AsyncSession,
) -> PostgreSQLLikeUnitOfWork:
    return Container.like_uow_factory(session=session)


"""
class PostgreSQLCreateUserUseCase(AbstractCreateUserUseCase):
    def __init__(self, uow_factory):
        # uow_factory — callable, возвращающая UoW через Depends
        self._uow_factory = uow_factory

    async def execute(self, schema: CreateUserSchema, uow: PostgreSQLUserUnitOfWork):
        # Мы ожидаем, что uow уже открыт (через Depends)
        author = await uow.repository.create(schema)
        return Container.author_uow_factory(author=author)
"""
