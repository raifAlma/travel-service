from abc import ABC, abstractmethod


class AbstractGetDetailRouteUseCase(ABC):
    @abstractmethod
    async def execute(self, route_id: int): ...
