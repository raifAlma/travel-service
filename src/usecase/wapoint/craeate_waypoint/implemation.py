from api.v1.way_points.models import WaypointSchema
from api.v1.users.models import CreateUpdateUserSchema
from .abstract import AbstractCreateWaypointUseCase
from fastapi import Depends, HTTPException

class PostgreSQLCreateWaypointUseCase(AbstractCreateWaypointUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, schema: WaypointSchema):

        async with self._uow as uow_:

            waypoint = await uow_.repository.create(schema)

        return waypoint
