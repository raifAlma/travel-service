from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession


from api.v1.way_points.models import WaypointUpdate, WaypointSchema

from infrastructure.database.postgresql.models.waypoints import Waypoint
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from infrastructure.repositories.postgres.waypoint.exception import WaypointNameIsNotUnique, RouteNotFound
from infrastructure.database.postgresql.models.Route import Route


class PostgreSQLWaypointRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, payload: WaypointSchema):
        smt = select(Waypoint).where(Waypoint.title == payload.title)
        result = await self._session.execute(smt)
        existing_route = result.scalar_one_or_none()
        if existing_route:
            raise WaypointNameIsNotUnique(field=payload.title)

        query = select(Route).where(Route.id == payload.route_id)
        result = await self._session.execute(query)
        route = result.scalar_one_or_none()
        if not route:
            raise RouteNotFound()


        waypoint = Waypoint(
            route_id=payload.route_id,
            title=payload.title,
            description=payload.description,
            latitude=payload.latitude,
            longitude=payload.longitude,
            #order_index=payload.order_index,
        )


        self._session.add(waypoint)
        #try:
        await self._session.flush()
        return waypoint
        #except IntegrityError as e:
         #       pattern = r'Key \((.*?)\)=\((.*?)\)'
          #      match = re.search(pattern, str(e))
           #     columns = [col.strip() for col in match.group(1).split(',')]
            #    values = [val.strip() for val in match.group(2).split(',')]
             #   raise RouteNameIsNotUnique(field=values[0])
        #return route


    async def delete(self, waypoint_id:int):
        waypoint = await self._session.get(Waypoint, waypoint_id)
        if waypoint is None:
            print(f"❌ [Repo] Точка {waypoint_id} не найден")
            raise HTTPException(status_code=404, detail="Waypoint not found")
        waypoint_data = WaypointSchema(latitude=waypoint.latitude, longitude=waypoint.longitude,
                                        title=waypoint.title, description=waypoint.description,
                                       route_id=waypoint.route_id)




        # result = UserSchema(id=user.id, name=user.name, email=user.email)
        try:
            await self._session.delete(waypoint)
            await self._session.flush()
            await self._session.commit()
            #print(f"✅ Пользователь {user_id} удален")
            #return waypoint_data
        except IntegrityError:
            await self._session.rollback()
            raise HTTPException(status_code=409, detail="Cannot delete waypoint")

    async def update(self, waypoint_id: int, payload: WaypointUpdate ) -> WaypointSchema:
        waypoint = await self._session.get(Waypoint, waypoint_id)
        if waypoint is None:
            raise HTTPException(status_code=404, detail="Waypoint not found")
            # Обновляем только те поля, которые пришли в payload
            # Используйте model_dump(exclude_unset=True) для Pydantic v2
        update_data = payload.model_dump(exclude_unset=True)
        if 'title' in update_data:
            new_title = update_data['title']
            if new_title is None:
                raise HTTPException(status_code=400, detail="Waypoint title cannot be null")
            stmt = select(Waypoint).where(Waypoint.title == new_title,
                                          Waypoint.id != waypoint_id)

            result = await self._session.execute(stmt)
            existing_waypoint = result.scalar_one_or_none()
            if existing_waypoint:
                raise WaypointNameIsNotUnique(field=new_title)


        for field, value in update_data.items():
            if hasattr(waypoint, field):
                setattr(waypoint, field, value)

        await self._session.commit()
        await self._session.refresh(waypoint)
        return WaypointSchema(latitude=waypoint.latitude, longitude=waypoint.longitude,
                              title=waypoint.title, description=waypoint.description, route_id=waypoint.route_id)


    async def get_by_id(self, waypoint_id: int) -> WaypointSchema:
        waypoint = await self._session.get(Waypoint, waypoint_id)
        if waypoint is None:
            raise HTTPException(status_code=404, detail="Waypoint not found")
        return WaypointSchema(latitude=waypoint.latitude, longitude=waypoint.longitude,
                              title=waypoint.title, description=waypoint.description, route_id=waypoint.route_id)