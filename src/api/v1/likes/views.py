from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix='/likes')

from .dependencies import create_like_use_case, build_like_unit_of_work
from usecase.comment.create_comment.abstarct import AbstractCreateCommentUseCase
from .models import LikeCreate




@router.post("", status_code=status.HTTP_201_CREATED)
async def create_like(
    payload: LikeCreate,
    usecase: AbstractCreateCommentUseCase= Depends(create_like_use_case),
) -> JSONResponse:
    try:
        like = await usecase.execute(payload)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return like
