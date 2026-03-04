import re
from enum import verify
from pyexpat.errors import messages

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.models import UserLoginSchema
from api.v1.users.crypto import context
from api.v1.users.models import CreateUpdateUserSchema, UserSchema
from infrastructure.database.postgresql.models.users import User
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from infrastructure.repositories.postgres.user.exception import UserIsExist, UserNotFound


class PostgreSQLUserRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session


    async def create(self, payload: CreateUpdateUserSchema):
        user = User(
            username=payload.username,
            email=payload.email,
            password=payload.password,
            age=payload.age,
        )
        self._session.add(user)
        try:
            await self._session.flush()
        except IntegrityError as e:
            pattern = r'Key \((.*?)\)=\((.*?)\)'
            match = re.search(pattern, str(e))
            columns = [col.strip() for col in match.group(1).split(',')]
            values = [val.strip() for val in match.group(2).split(',')]
            raise UserIsExist(field=columns[0], value=values[0])
        return UserSchema(id=user.id, username=user.username, age=user.age, email=user.email)


    async def get_by_id(self, user_id: int) -> User:
        user = await self._session.get(User, user_id)
        if user is not None:
            user = UserSchema(id=user.id, username=user.username, age=user.age, email=user.email)
            return user
        raise HTTPException(status_code=404, detail="User not found")

    async def delete (self, user_id) -> UserSchema:
        user = await self._session.get(User, user_id)
        if user is None:
            print(f"❌ [Repo] Пользователь {user_id} не найден")
            raise HTTPException(status_code=404, detail="User not found")
        user_data = UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            age=user.age
        )

        #result = UserSchema(id=user.id, name=user.name, email=user.email)
        try:
            await self._session.delete(user)
            await self._session.flush()
            await self._session.commit()
            print(f"✅ Пользователь {user_id} удален")
            return user_data
        except IntegrityError:
            await self._session.rollback()
            raise HTTPException(status_code=409, detail="Cannot delete user")

    async def update(self, user_id: int, payload: CreateUpdateUserSchema) -> User:
        user = await self._session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user.username = payload.username
        user.age = payload.age
        user.email = payload.email
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

    async def authorize(self, schema: UserLoginSchema) -> UserSchema | None:
        query = select(User).where(and_(User.username == schema.username))
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()

        if user is None:
            raise UserNotFound()

        verify = context.verify(schema.password, user.password)
        print(f"Username: {schema.username}")
        print(f"Password from request: {schema.password}")
        print(f"Password hash from DB: {user.password}")
        print(f"Verify result: {verify}")

        if not verify:
                raise HTTPException(status_code=400, detail="Incorrect password")

        return UserSchema(id=user.id, username=user.username, age=user.age, email=user.email)
            #raise UserNotFound()












