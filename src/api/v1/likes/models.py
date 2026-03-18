from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

class LikeCreate(BaseModel):
    route_id: int
    user_id: int

class LikeResponse(LikeCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int

class OwnerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str

class LikeOwnerResponse(LikeResponse):
    owner: OwnerSchema

