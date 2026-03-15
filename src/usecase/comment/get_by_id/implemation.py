from .abstract import AbstractGetCommentUseCase


class PostgreSQLGetCommentUseCase(AbstractGetCommentUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, commnt_id: int):

        async with self._uow as uow_:

            user = await uow_.repository.get_by_id(commnt_id)
        return user