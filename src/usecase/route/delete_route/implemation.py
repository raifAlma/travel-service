from api.v1.routes.models import RouteBase
from api.v1.users.models import CreateUpdateUserSchema
from .abstract import AbstractDeleteRouteUseCase
from fastapi import Depends, HTTPException

class PostgreSQLDeleteRouteUseCase(AbstractDeleteRouteUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, route_id:int):

        async with self._uow as uow_:

            route = await uow_.repository.delete(route_id)
        return route