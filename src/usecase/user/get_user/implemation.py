from api.v1.routes.models import RouteCreate, RouteResponse
from api.v1.users.models import CreateUpdateUserSchema, UserSchema
from .abstract import AbstractGetUserUseCase
from fastapi import Depends, HTTPException

class PostgreSQLGetUserUseCase(AbstractGetUserUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int):

        async with self._uow as uow_:

            user = await uow_.repository.get_by_id(user_id)
        return user