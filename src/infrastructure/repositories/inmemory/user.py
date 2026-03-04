from typing import Dict, Optional, List

from sqlalchemy.exc import IntegrityError

from api.v1.users.models import CreateUpdateUserSchema, UserSchema
from domain.user.models import User, UserCreateDTO,UserUpdateDTO
from domain.user.repository import AbstractUserRepository
from fastapi.exceptions import HTTPException



class InMemoryUserRepository(AbstractUserRepository):
    async def create(self, payload: CreateUpdateUserSchema):
        user = User(
            rname=payload.name,
            age=payload.age,
            # gender=Gender.male,
            email=payload.email,
            password = payload.password

        )
        self._session.add(user)
        try:
            await self._session.flush()
            await self._session.commit()
        except IntegrityError as exc:
            await self._session.rollback()
            raise HTTPException(status_code=400, detail="Could not create user")
        return UserSchema(id=user.id, username=user.name, age=user.age, email=user.email)

    async def get_by_id(self, user_id: int) -> User:
        user = await self._session.get(User, user_id)
        if user is not None:
            user = UserSchema(id=user.id, name=user.name, email=user.email)
            return user
        raise HTTPException(status_code=404, detail="User not found")

    async def get_by_name(self, name: str) -> User:
        ...

    async def delete(self, user_id: int) -> UserSchema:
        user = await self._session.get(User, user_id)
        result = UserSchema(id=user.id, name=user.name, age=user.age, email=user.email)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        result = UserSchema( name=user.name, age=user.age, email=user.email)

        try:
            await self._session.delete(user)
            await self.session.commit()
            return result
        except IntegrityError as exc:
            self._session.rollback()
            raise HTTPException(status_code=400, detail="Could not delete user")
            #return result

    async def update(self, user_id: int, payload: CreateUpdateUserSchema) -> User:
        user = await self._session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        user.name = payload.name
        user.age = payload.age
        user.email = payload.email
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return user

