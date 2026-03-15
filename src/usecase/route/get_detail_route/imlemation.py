from api.v1.routes.models import RouteDetailResponse
from .abstract import AbstractGetDetailRouteUseCase


class PostgreSQLGetDetailRouteUseCase(AbstractGetDetailRouteUseCase):
    def __init__(self, uow):
        self._uow = uow

    async def execute(self, route_id: int) -> RouteDetailResponse:

        async with self._uow as uow_:

            route = await uow_.repository.get_detail_by_id(route_id)
        return route