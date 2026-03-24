import re

from api.v1.auth.models import UserLoginSchema
from api.v1.users.crypto import context, hash_password
from api.v1.users.models import CreateUserSchema, UserSchema, UpdateUserSchema
from fastapi import HTTPException
from infrastructure.database.postgresql.models.users import User
from infrastructure.repositories.postgres.user.exception import (UserIsExist,NameIsNotUnique,
                                                                 UserNotFound, EmailIsNotUnique)
from sqlalchemy import and_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession


class PostgreSQLUserRepository:
    def __init__(self, session: AsyncSession):
        self._session: AsyncSession = session

    async def create(self, payload: CreateUserSchema):
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
            pattern = r"Key \((.*?)\)=\((.*?)\)"
            match = re.search(pattern, str(e))
            columns = [col.strip() for col in match.group(1).split(",")]
            values = [val.strip() for val in match.group(2).split(",")]
            raise UserIsExist(field=columns[0], value=values[0])
        return UserSchema(
            id=user.id, username=user.username, age=user.age, email=user.email
        )

    async def get_by_id(self, user_id: int) -> User:
        user = await self._session.get(User, user_id)
        if user is not None:
            user = UserSchema(
                id=user.id, username=user.username, age=user.age, email=user.email
            )
            return user
        raise HTTPException(status_code=404, detail="User not found")

    async def delete(self, user_id) -> None:
        user = await self._session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        try:
            await self._session.delete(user)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Cannot delete user")

    async def update(self, user_id: int, payload: UpdateUserSchema) -> UserSchema:
        user = await self._session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        update_data = payload.model_dump(exclude_unset=True)
        if 'email' in update_data:
            new_email = update_data['email']
            if new_email is None:
                raise HTTPException(status_code=400, detail="Email cannot be null")
            smt = select(User).where(User.email == new_email, User.id != user_id)
            result = await self._session.execute(smt)
            existing_email = result.scalar_one_or_none()
            if existing_email:
                raise EmailIsNotUnique (field=new_email)

        if 'username' in update_data:
            new_username = update_data['username']
            if new_username is None:
                raise HTTPException(status_code=400, detail="Username cannot be null")
            smt = select(User).where(User.username == new_username, User.id != user_id)
            result = await self._session.execute(smt)
            existing_username = result.scalar_one_or_none()
            if existing_username:
                raise NameIsNotUnique(field=new_username)

        if 'password' in update_data:
            new_password = update_data['password']
            if new_password is None:
                raise HTTPException(status_code=400, detail="Password cannot be null")
            update_data['password'] = hash_password(new_password)

        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)
        await self._session.refresh(user)
        return UserSchema(
            id=user.id, username=user.username, age=user.age, email=user.email
        )

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

        return UserSchema(
            id=user.id, username=user.username, age=user.age, email=user.email
        )
