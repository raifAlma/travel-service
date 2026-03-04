from abc import ABC, abstractmethod

from api.v1.way_points.models import WaypointSchema


class AbstractGetWaypointUseCase(ABC):
    @abstractmethod
    async def execute(self, schema: WaypointSchema):
        ...