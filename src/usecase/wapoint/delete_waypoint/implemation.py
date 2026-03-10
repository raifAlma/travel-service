from .abstract import AbstractDeleteWaypointUseCase

class PostgreSQLDeleteWaypointUseCase(AbstractDeleteWaypointUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, waypoint_id:int):

        async with self._uow as uow_:

            waypoint = await uow_.repository.delete(waypoint_id)
        return waypoint