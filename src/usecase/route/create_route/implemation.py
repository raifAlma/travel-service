from api.v1.routes.models import RouteCreate
from api.v1.users.models import CreateUpdateUserSchema
from .abstarct import AbstractCreateRouteUseCase
from fastapi import Depends, HTTPException

class PostgreSQLCreateRouteUseCase(AbstractCreateRouteUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: RouteCreate):

        async with self._uow as uow_:

            route = await uow_.repository.create(schema)
        return route