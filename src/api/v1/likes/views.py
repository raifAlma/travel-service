from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from usecase.like.add_like.abstract import AbstractAddLikeeUseCase
from usecase.like.delete_like.abstract import AbstractDeleteLikeUseCase

from .dependencies import create_like_use_case, delete_like_use_case
from .models import LikeCreateDelete


router = APIRouter(prefix="/likes")


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_like(
    payload: LikeCreateDelete,
    usecase: AbstractAddLikeeUseCase = Depends(create_like_use_case),
) -> JSONResponse:
    try:
        like = await usecase.execute(payload)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return like


@router.delete("/{like_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_like(
    like_id: int, usecase: AbstractDeleteLikeUseCase = Depends(delete_like_use_case)
):
    await usecase.execute(like_id)
    return None
