from abc import ABC, abstractmethod

from api.v1.routes.models import RouteCreate


class AbstractGetUserUseCase(ABC):
    @abstractmethod
    async def execute(self,  user_id: int):
        ...