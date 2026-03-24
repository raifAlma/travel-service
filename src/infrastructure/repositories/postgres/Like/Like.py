from api.v1.likes.models import LikeCreateDelete
from fastapi import HTTPException
from infrastructure.database.postgresql.models.like import Likes
from infrastructure.repositories.postgres.Like.exception import \
    LikeAlreadyExists
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


# from .exception  import RouteNameIsNotUnique, UserNotAuthorize


class PostgreSQLLikeRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def add_like(self, payload: LikeCreateDelete):
        like = Likes(user_id=payload.user_id, route_id=payload.route_id)
        self._session.add(like)
        try:
            await self._session.flush()
        except IntegrityError:
            raise LikeAlreadyExists()
        return like

    async def delete_like(self, like_id: int):
        like = await self._session.get(Likes, like_id)
        if like is None:
            raise HTTPException(status_code=404, detail="Like not found")
        try:
            await self._session.delete(like)
            await self._session.flush()
            await self._session.commit()
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Cannot delete like")
