from pydantic import BaseModel, Field

class CommentCreate(BaseModel):
    user_id: int
    route_id: int
    comment_text: str = Field(..., min_length=10, max_length=50)


class CommentResponse(CommentCreate):
    id: int


