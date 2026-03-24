from api.v1.comments.models import CommentCreate

from .abstarct import AbstractCreateCommentUseCase


class PostgreSQLCreateCommentUseCase(AbstractCreateCommentUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: CommentCreate):

        async with self._uow as uow_:

            comment = await uow_.repository.create(schema)
        return comment
