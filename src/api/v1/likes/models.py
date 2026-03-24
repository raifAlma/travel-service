from pydantic import BaseModel, ConfigDict


class LikeCreateDelete(BaseModel):
    route_id: int
    user_id: int


class LikeResponse(LikeCreateDelete):
    id: int


class OwnerSchema(BaseModel):
    id: int
    username: str


class LikeOwnerResponse(LikeResponse):
    owner: OwnerSchema
