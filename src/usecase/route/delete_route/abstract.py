from abc import ABC, abstractmethod

from api.v1.routes.models import RouteBase


class AbstractDeleteRouteUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: RouteBase):
        ...