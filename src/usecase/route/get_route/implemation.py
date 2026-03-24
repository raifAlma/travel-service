from api.v1.routes.models import RouteResponse

from .abstract import AbstractGetRouteUseCase


class PostgreSQLGetRouteUseCase(AbstractGetRouteUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: RouteResponse):

        async with self._uow as uow_:

            route = await uow_.repository.get_by_id(schema)
        return route
