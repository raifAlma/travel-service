from urllib.parse import parse_qsl

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from infrastructure.database.postgresql.models.like import Likes
from api.v1.likes.models import LikeCreate, LikeResponse
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


from infrastructure.repositories.postgres.Like.exception import LikeAlreadyExists


#from .exception  import RouteNameIsNotUnique, UserNotAuthorize



class PostgreSQLLikeRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def add_like(self, payload: LikeCreate):
        like = Likes(user_id = payload.user_id, route_id = payload.route_id)
        self._session.add(like)
        try:
            await self._session.flush()
        except IntegrityError:
            raise LikeAlreadyExists()
        return like



