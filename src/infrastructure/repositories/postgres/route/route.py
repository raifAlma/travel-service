from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.postgresql.models.users import User
from api.v1.routes.models import RouteCreate, RouteUpdate, RouteResponse, RouteBase
from infrastructure.database.postgresql.models.Route import Route

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from .exception  import RouteNameIsNotUnique, UserNotAuthorize



class PostgreSQLRouteRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, payload: RouteCreate):
        smt = select(Route).where(Route.title == payload.title)
        result = await self._session.execute(smt)
        existing_route = result.scalar_one_or_none()
        if existing_route:
            raise RouteNameIsNotUnique(field=payload.title)

        query = select(User).where(User.id == payload.owner_id)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotAuthorize()

        route = Route(
            owner_id=payload.owner_id,
            title=payload.title,
            description=payload.description,
            difficulty=payload.difficulty,
            distance_km=payload.distance_km,
            estimated_hours=payload.estimated_hours,

        )
        self._session.add(route)
        await self._session.flush()
        return route

    async def get_by_id(self, route_id: int) -> RouteResponse:
        route = await self._session.get(Route, route_id)
        if route is not None:
            route = RouteResponse(id=route.id, title=route.title,
                                  difficulty=route.difficulty, owner_id=route.owner_id, description=route.description)
            return route
        raise HTTPException(status_code=404, detail="Route not found")

    async def delete(self, route_id:int) -> None:
        route = await self._session.get(Route, route_id)
        if route is None:
            raise HTTPException(status_code=404, detail="Route not found")
        try:
            await self._session.delete(route)
            await self._session.flush()
            await self._session.commit()
        except IntegrityError:
            await self._session.rollback()
            raise HTTPException(status_code=409, detail="Cannot delete route")

    async def update(self, route_id: int, payload: RouteUpdate) -> RouteResponse:
        route = await self._session.get(Route, route_id)
        if route is None:
            raise HTTPException(status_code=404, detail="Route not found")
            # Обновляем только те поля, которые пришли в payload
            # Используйте model_dump(exclude_unset=True) для Pydantic v2
        update_data = payload.model_dump(exclude_unset=True)
        if 'title' in update_data:
            new_title = update_data['title']
            if new_title is None:
                raise HTTPException(status_code=409, detail="Route title cannot be null")
            smt = select(Route).where(Route.title == new_title, Route.id != route_id)

            result = await self._session.execute(smt)
            existing_route = result.scalar_one_or_none()
            if existing_route:
                raise RouteNameIsNotUnique(field=new_title)

        for field, value in update_data.items():
            if hasattr(route, field):
                setattr(route, field, value)
        await self._session.commit()
        await self._session.refresh(route)
        return RouteResponse(id=route.id, title=route.title,
                             difficulty=route.difficulty, owner_id=route.owner_id, description=route.description)




