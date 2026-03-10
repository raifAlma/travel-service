from api.v1.way_points.models import WaypointSchema
from .abstract import AbstractGetWaypointUseCase

class PostgreSQLGetRouteUseCase(AbstractGetWaypointUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: WaypointSchema):

        async with self._uow as uow_:

            waypoint = await uow_.repository.get_by_id(schema)
        return waypoint