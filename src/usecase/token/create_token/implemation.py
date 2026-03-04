from api.v1.auth.models import UserLoginSchema
from api.v1.users.models import CreateUpdateUserSchema
from .abstract import AbstractCreateTokenUseCase
from fastapi import Depends, HTTPException

class PostgreSQLCreateTokenUseCase(AbstractCreateTokenUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: UserLoginSchema):
        async with self._uow as uow_:
            user = await uow_.user_repository.authorize(schema)
            token = await uow_.repository.create(user)

        return token