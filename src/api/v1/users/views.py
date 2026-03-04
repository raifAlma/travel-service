from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.postgresql.session import get_async_session
from infrastructure.repositories.postgres.user.exception import UserIsExist
from infrastructure.repositories.postgres.user.uow import PostgreSQLUserUnitOfWork
from infrastructure.repositories.postgres.user import PostgreSQLUserRepository
from usecase.user.create_user.implemation import PostgreSQLCreateUserUseCase
from usecase.user.create_user.abstarct import AbstractCreateUserUseCase
from usecase.user.get_user.abstract import AbstractGetUserUseCase
from usecase.user.delete_user.abstract import AbstractDeleteUserUseCase
from usecase.user.update_user.abstract import AbstractUpdateUserUseCase
from .dependencies import get_user_unit_of_work, create_user_use_case, delete_user_use_case, update_user_use_case, get_user_use_case
from .models import CreateUpdateUserSchema, UserSchema

router = APIRouter(prefix='/users')

security_scheme = HTTPBearer(scheme_name="Bearer")

@router.post("", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: CreateUpdateUserSchema,
    usecase: AbstractCreateUserUseCase = Depends(create_user_use_case),
) -> JSONResponse:
    try:
        user = await usecase.execute(payload)
    except UserIsExist as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=user.model_dump())


@router.get("/{id}", response_model=UserSchema)
async def get_user_by_id(id: int,
                         usecase: AbstractGetUserUseCase = Depends(get_user_use_case)

) -> JSONResponse:
    try:
        user = await usecase.execute(id)
    except UserIsExist as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return JSONResponse(content=jsonable_encoder(user))


@router.delete("/{id}")
async def delete_user_by_id(id: int,
        usecase: AbstractDeleteUserUseCase = Depends(delete_user_use_case),
):
        await usecase.execute(id)
        return None
@router.put("/{user_id}")
async def update_user_by_id(id: int,
        payload: CreateUpdateUserSchema,
        usecase: AbstractUpdateUserUseCase = Depends(update_user_use_case),
):
    try:
        user = await usecase.execute(id, payload)
        return JSONResponse(content=jsonable_encoder(user))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get("/me", response_model=UserSchema)
async def get_user_me(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)) -> JSONResponse:
    #repo = PostgreSQLUserRepository(session)
    #user = await repo.get(id)
    return
        #(
        #JSONResponse(status_code=status.HTTP_200_OK, content=user.model_dump()))




