from api.v1.users.models import CreateUpdateUserSchema
from .abstarct import AbstractCreateUserUseCase


class PostgreSQLCreateUserUseCase(AbstractCreateUserUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: CreateUpdateUserSchema):
        async with self._uow as uow_:

            user = await uow_.repository.create(schema)

        return user