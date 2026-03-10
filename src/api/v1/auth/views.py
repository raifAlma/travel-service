from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from infrastructure.repositories.postgres.token.exception import InvalidRefreshToken
from usecase.token.create_token.abstract import AbstractCreateTokenUseCase
from .dependencies import create_token_use_case, refresh_token_use_case
from usecase.token.refresh_token.abstract import AbstractRefreshTokenUseCase
from .models import UserLoginSchema, TokenSchema, RefreshTokenSchema
from infrastructure.repositories.postgres.user.exception import UserNotFound

router = APIRouter(prefix='/auth')



@router.post("/token", response_model = TokenSchema, status_code=status.HTTP_201_CREATED)
async def create_token(
    payload: UserLoginSchema,
    usecase: AbstractCreateTokenUseCase = Depends(create_token_use_case),
) -> JSONResponse:

    try:
        token = await usecase.execute(payload)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=token.model_dump(mode='json'))


@router.post("/token/refresh", response_model=TokenSchema, status_code=status.HTTP_201_CREATED)
async def refresh_token(
        payload: RefreshTokenSchema,
        usecase: AbstractRefreshTokenUseCase = Depends(refresh_token_use_case),
) -> JSONResponse:
    try:
        token = await usecase.execute(payload)
    except InvalidRefreshToken as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=token.model_dump(mode='json'))


