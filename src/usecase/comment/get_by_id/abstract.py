from abc import ABC, abstractmethod


class AbstractGetCommentUseCase(ABC):
    @abstractmethod
    async def execute(self, commnt_id: int): ...
