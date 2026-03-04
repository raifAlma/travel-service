from api.v1.routes.models import RouteBase
from api.v1.users.models import CreateUpdateUserSchema
from .abstract import AbstractDeleteUserUseCase
from fastapi import Depends, HTTPException

class PostgreSQLDeleteUserUseCase(AbstractDeleteUserUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id:int):

        async with self._uow as uow_:

            user = await uow_.repository.delete(user_id)
        return user