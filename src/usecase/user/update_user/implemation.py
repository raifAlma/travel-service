from api.v1.users.models import UpdateUserSchema

from .abstract import AbstractUpdateUserUseCase


class PostgreSQLUpdateUserUseCase(AbstractUpdateUserUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int, schema: UpdateUserSchema):

        async with self._uow as uow_:

            user = await uow_.repository.update(user_id, schema)
        return user
