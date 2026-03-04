from api.v1.routes.models import RouteBase
from api.v1.users.models import CreateUpdateUserSchema
from .abstract import AbstractDeleteWaypointUseCase
from fastapi import Depends, HTTPException

class PostgreSQLDeleteWaypointUseCase(AbstractDeleteWaypointUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, waypoint_id:int):

        async with self._uow as uow_:

            waypoint = await uow_.repository.delete(waypoint_id)
        return waypoint