from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton, Factory

from infrastructure.database.postgresql.session_manager import DatabaseSessionManager
from infrastructure.repositories.postgres.route import PostgreSQLRouteUnitOfWork
from infrastructure.repositories.postgres.user.uow import PostgreSQLUserUnitOfWork
from infrastructure.repositories.postgres.token.uow import PostgreSQLTokenUnitOfWork
from infrastructure.repositories.postgres.waypoint.uow import PostgreSQLWaypointUnitOfWork

class Container(DeclarativeContainer):
    session_manager = Singleton(DatabaseSessionManager)

    user_uow_factory = Factory(PostgreSQLUserUnitOfWork)
    token_uow_factory = Factory(PostgreSQLTokenUnitOfWork)
    route_uow_factory = Factory(PostgreSQLRouteUnitOfWork)
    waypoint_uow_factory = Factory(PostgreSQLWaypointUnitOfWork)