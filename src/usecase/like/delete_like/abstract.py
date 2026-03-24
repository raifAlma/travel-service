from abc import ABC, abstractmethod

from api.v1.likes.models import LikeCreateDelete


class AbstractDeleteLikeUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: LikeCreateDelete): ...
