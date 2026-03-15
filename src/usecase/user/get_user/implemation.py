
from .abstract import AbstractGetUserUseCase


class PostgreSQLGetUserUseCase(AbstractGetUserUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id: int):

        async with self._uow as uow_:

            comment = await uow_.repository.get_by_id(user_id)
        return comment