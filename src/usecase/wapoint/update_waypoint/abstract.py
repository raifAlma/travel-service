from abc import ABC, abstractmethod

from api.v1.way_points.models import WaypointSchema


class AbstractUpdateWaypointUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: WaypointSchema):
        ...