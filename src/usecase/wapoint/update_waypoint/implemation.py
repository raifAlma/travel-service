from api.v1.way_points.models import WaypointUpdate
from api.v1.users.models import CreateUpdateUserSchema
from .abstract import AbstractUpdateWaypointUseCase
from fastapi import Depends, HTTPException

class PostgreSQLUpdateWaypointUseCase(AbstractUpdateWaypointUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, waypoint_id: int, schema: WaypointUpdate):

        async with self._uow as uow_:

            waypoint = await uow_.repository.update(waypoint_id,schema)
        return waypoint