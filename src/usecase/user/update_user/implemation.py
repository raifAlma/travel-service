from api.v1.routes.models import RouteCreate, RouteResponse, RouteUpdate

from api.v1.users.models import CreateUpdateUserSchema
from .abstract import AbstractUpdateUserUseCase
from fastapi import Depends, HTTPException

class PostgreSQLUpdateUserUseCase(AbstractUpdateUserUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, schema: CreateUpdateUserSchema):

        async with self._uow as uow_:

            user = await uow_.repository.update(user_id,schema)
        return user