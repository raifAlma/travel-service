from abc import ABC, abstractmethod

from api.v1.comments.models import CommentCreate


class AbstractCreateCommentUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: CommentCreate): ...
