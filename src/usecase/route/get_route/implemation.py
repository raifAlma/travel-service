from api.v1.routes.models import RouteCreate, RouteResponse
from api.v1.users.models import CreateUpdateUserSchema
from .abstract import AbstractGetRouteUseCase
from fastapi import Depends, HTTPException

class PostgreSQLGetRouteUseCase(AbstractGetRouteUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: RouteResponse):

        async with self._uow as uow_:

            route = await uow_.repository.get_by_id(schema)
        return route