from .abstract import AbstractDeleteLikeUseCase


class PostgreSQLDeleteLikeUseCase(AbstractDeleteLikeUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, like_id: int):

        async with self._uow as uow_:

            like = await uow_.repository.delete_like(like_id)
        return like
