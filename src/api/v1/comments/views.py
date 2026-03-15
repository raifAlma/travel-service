from fastapi import status, APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from usecase.comment.get_by_id.abstract import AbstractGetCommentUseCase
from .dependencies import create_comment_use_case, get_comment_by_id_use_case
from usecase.comment.create_comment.abstarct import AbstractCreateCommentUseCase
from .models import CommentCreate, CommentResponse

router = APIRouter(prefix='/comments')


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_comment(
    payload: CommentCreate,
    usecase: AbstractCreateCommentUseCase= Depends(create_comment_use_case),
) -> JSONResponse:
    try:
        comment = await usecase.execute(payload)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return comment

@router.get("{id}", response_model=CommentResponse, status_code=status.HTTP_200_OK)
async def get_comment_by_id(
        id: int,
        usecase: AbstractGetCommentUseCase = Depends(get_comment_by_id_use_case)
) -> JSONResponse:
    try:
        comment = await usecase.execute(id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return comment
