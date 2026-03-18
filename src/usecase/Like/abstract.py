from abc import ABC, abstractmethod

from api.v1.likes.models import LikeCreate


class AbstractAddLikeeUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: LikeCreate):
        ...