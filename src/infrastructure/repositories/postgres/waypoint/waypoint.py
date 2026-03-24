from api.v1.way_points.models import WaypointSchema, WaypointUpdate
from fastapi import HTTPException
from infrastructure.database.postgresql.models.Route import Route
from infrastructure.database.postgresql.models.waypoints import Waypoint
from infrastructure.repositories.postgres.waypoint.exception import (
    RouteNotFound, WaypointNameIsNotUnique,)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


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
        )

        self._session.add(waypoint)
        await self._session.flush()
        return waypoint

    async def delete(self, waypoint_id: int) -> None:
        waypoint = await self._session.get(Waypoint, waypoint_id)
        if waypoint is None:
            raise HTTPException(status_code=404, detail="Waypoint not found")
        try:
            await self._session.delete(waypoint)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Cannot delete waypoint")

    async def update(self, waypoint_id: int, payload: WaypointUpdate) -> WaypointSchema:
        waypoint = await self._session.get(Waypoint, waypoint_id)
        if waypoint is None:
            raise HTTPException(status_code=404, detail="Waypoint not found")
        update_data = payload.model_dump(exclude_unset=True)
        if "title" in update_data:
            new_title = update_data["title"]
            if new_title is None:
                raise HTTPException(
                    status_code=400, detail="Waypoint title cannot be null"
                )
            stmt = select(Waypoint).where(
                Waypoint.title == new_title, Waypoint.id != waypoint_id
            )

            result = await self._session.execute(stmt)
            existing_waypoint = result.scalar_one_or_none()
            if existing_waypoint:
                raise WaypointNameIsNotUnique(field=new_title)

        for field, value in update_data.items():
            if hasattr(waypoint, field):
                setattr(waypoint, field, value)

        await self._session.refresh(waypoint)
        return WaypointSchema(
            latitude=waypoint.latitude,
            longitude=waypoint.longitude,
            title=waypoint.title,
            description=waypoint.description,
            route_id=waypoint.route_id,
        )

    async def get_by_id(self, waypoint_id: int) -> WaypointSchema:
        waypoint = await self._session.get(Waypoint, waypoint_id)
        if waypoint is None:
            raise HTTPException(status_code=404, detail="Waypoint not found")
        return WaypointSchema(
            latitude=waypoint.latitude,
            longitude=waypoint.longitude,
            title=waypoint.title,
            description=waypoint.description,
            route_id=waypoint.route_id,
        )
