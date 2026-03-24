from abc import ABC, abstractmethod

from api.v1.routes.models import RouteCreate


class AbstractGetRouteUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: RouteCreate): ...
