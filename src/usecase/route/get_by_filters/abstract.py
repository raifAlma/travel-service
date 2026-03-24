from abc import ABC, abstractmethod

from api.pydantic.models import RouteFilters


class AbstractGetByFiltersRouteUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: RouteFilters): ...
