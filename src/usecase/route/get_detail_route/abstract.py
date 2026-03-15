from abc import ABC, abstractmethod

from api.v1.routes.models import RouteDetailResponse


class AbstractGetDetailRouteUseCase(ABC):
    @abstractmethod
    async def execute(self, route_id: int):
        ...