from api.v1.routes.models import RouteUpdate

from .abstract import AbstractUpdateRouteUseCase


class PostgreSQLUpdateRouteUseCase(AbstractUpdateRouteUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, route_id: int, schema: RouteUpdate):

        async with self._uow as uow_:

            route = await uow_.repository.update(route_id, schema)
        return route
