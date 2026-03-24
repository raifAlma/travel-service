from api.v1.likes.models import LikeCreateDelete

from .abstract import AbstractAddLikeeUseCase


class PostgreSQLAddLikeUseCase(AbstractAddLikeeUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: LikeCreateDelete):

        async with self._uow as uow_:

            like = await uow_.repository.add_like(schema)
        return like
