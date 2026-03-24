from api.pydantic.models import RouteFilters
from infrastructure.database.postgresql.models import Route

from .abstract import AbstractGetByFiltersRouteUseCase


class PostgreSQLGetByFiltersRouteUseCase(AbstractGetByFiltersRouteUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: RouteFilters) -> tuple[list[Route], int]:

        async with self._uow as uow_:

            route = await uow_.repository.get_route_by_filters(schema)
        return route
