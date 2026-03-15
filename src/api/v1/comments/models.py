from pydantic import BaseModel, Field, ConfigDict

from api.v1.users.models import UserInfoSchema


class CommentCreate(BaseModel):
    user_id: int
    route_id: int
    comment_text: str = Field(..., min_length=10, max_length=50)


class CommentResponse(BaseModel):
    id: int
    comment_text: str
    user: UserInfoSchema
    route_id: int

    model_config = ConfigDict(from_attributes=True)


