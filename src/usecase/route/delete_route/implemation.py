
from .abstract import AbstractDeleteRouteUseCase
class PostgreSQLDeleteRouteUseCase(AbstractDeleteRouteUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, route_id:int):

        async with self._uow as uow_:

            route = await uow_.repository.delete(route_id)
        return route