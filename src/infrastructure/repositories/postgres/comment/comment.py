from fastapi import HTTPException
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from infrastructure.database.postgresql.models import Waypoint, Route
from infrastructure.database.postgresql.models.users import User
from api.v1.comments.models import CommentCreate, CommentResponse
from infrastructure.database.postgresql.models.Comment import Comments
from infrastructure.repositories.postgres.comment.exception import UserNotAuthorize, RouteNotFound





class PostgreSQLCommentRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, payload: CommentCreate):
        query = select(User).where(User.id == payload.user_id)
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            raise UserNotAuthorize()

        smt = select(Route).where(Route.id == payload.route_id)
        result = await self._session.execute(smt)
        route = result.scalar_one_or_none()
        if not route:
            raise RouteNotFound
        comment = Comments(
            user_id = payload.user_id,
            comment_text = payload.comment_text,
            route_id = payload.route_id

        )

        self._session.add(comment)
        await self._session.flush()
        return CommentResponse (id = comment.id, comment_text = comment.comment_text, route_id = comment.route_id,
                                user_id = comment.user_id)

    async def get_by_id(self, comment_id: int)-> CommentResponse:
        stmt = (select(Comments).options(selectinload(Comments.user)).where(Comments.id == comment_id))
        result = await self._session.execute(stmt)
        comment = result.scalar_one_or_none()
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return CommentResponse (id = comment.id, comment_text = comment.comment_text,
                                user=comment.user, route_id = comment.route_id)




