from api.pydantic.models import RouteFilters
from api.v1.routes.models import (RouteCreate, RouteDetailResponse,
                                  RouteResponse, RouteUpdate,)
from fastapi import HTTPException
from infrastructure.database.postgresql.models import Comments
from infrastructure.database.postgresql.models.Route import Route
from infrastructure.database.postgresql.models.users import User
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .exception import RouteNameIsNotUnique, UserNotAuthorize


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
            route = RouteResponse(
                id=route.id,
                title=route.title,
                difficulty=route.difficulty,
                owner_id=route.owner_id,
                description=route.description,
            )
            return route
        raise HTTPException(status_code=404, detail="Route not found")

    async def get_detail_by_id(self, route_id: int) -> RouteDetailResponse:
        stmt = (
            select(Route)
            .options(
                selectinload(Route.waypoints),
                selectinload(Route.comments).selectinload(Comments.user),
                selectinload(Route.owner),
            )
            .where(Route.id == route_id)
        )
        result = await self._session.execute(stmt)
        route = result.scalar_one_or_none()
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
        return RouteDetailResponse.model_validate(route)

    async def get_route_by_filters(
        self, filters: RouteFilters
    ) -> tuple[list[Route], int]:
        stmt = select(Route)

        if filters.title:
            stmt = stmt.where(Route.title.ilike(f"%{filters.title}%"))
        if filters.difficulties:
            stmt = stmt.where(Route.difficulty.in_(filters.difficulties))
        if filters.distance_min is not None:
            stmt = stmt.where(Route.distance_km >= filters.distance_min)
        if filters.distance_max is not None:
            stmt = stmt.where(Route.distance_km <= filters.distance_max)
        if filters.duration_min is not None:
            stmt = stmt.where(Route.estimated_hours >= filters.duration_min)
        if filters.duration_max is not None:
            stmt = stmt.where(Route.estimated_hours <= filters.duration_max)

        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self._session.scalar(count_stmt)

        if filters.sort_by:
            if filters.sort_by == "title":
                order_col = Route.title
            elif filters.sort_by == "distance":
                order_col = Route.distance_km
            elif filters.sort_by == "duration":
                order_col = Route.estimated_hours
            else:
                order_col = Route.id

            if filters.order == "desc":
                order_col = order_col.desc()
            stmt = stmt.order_by(order_col)

            # Пагинация
        stmt = stmt.limit(filters.limit).offset(filters.offset)

        result = await self._session.execute(stmt)
        routes = result.scalars().all()
        return routes, total

    async def delete(self, route_id: int) -> None:
        route = await self._session.get(Route, route_id)
        if route is None:
            raise HTTPException(status_code=404, detail="Route not found")
        try:
            await self._session.delete(route)
            await self._session.flush()
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Cannot delete route")

    async def update(self, route_id: int, payload: RouteUpdate) -> RouteResponse:
        route = await self._session.get(Route, route_id)
        if route is None:
            raise HTTPException(status_code=404, detail="Route not found")
        update_data = payload.model_dump(exclude_unset=True)
        if "title" in update_data:
            new_title = update_data["title"]
            if new_title is None:
                raise HTTPException(
                    status_code=409, detail="Route title cannot be null"
                )
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
        return RouteResponse(
            id=route.id,
            title=route.title,
            difficulty=route.difficulty,
            owner_id=route.owner_id,
            description=route.description,
        )
