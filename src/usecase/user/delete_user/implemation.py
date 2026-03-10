from .abstract import AbstractDeleteUserUseCase

class PostgreSQLDeleteUserUseCase(AbstractDeleteUserUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, user_id:int):

        async with self._uow as uow_:

            user = await uow_.repository.delete(user_id)
        return user