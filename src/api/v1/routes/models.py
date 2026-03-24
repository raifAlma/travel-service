from enum import Enum
from typing import List, Optional

from api.v1.comments.models import CommentResponse
from api.v1.way_points.models import WaypointSchema
from pydantic import BaseModel, ConfigDict, Field


# from api.pydantic.models import RouteFilters


class DifficultyEnum(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"
    UNSPECIFIED = "unspecified"


class RouteBase(BaseModel):
    owner_id: int
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    difficulty: DifficultyEnum = Field(default=DifficultyEnum.MEDIUM)
    distance_km: Optional[float] = Field(None, ge=0.1, le=1000)
    estimated_hours: Optional[float] = Field(None, ge=0.1, le=240)


class RouteCreate(RouteBase):
    # Поля те же, что в RouteBase
    pass


class RouteUpdate(BaseModel):
    # Для обновления все поля опциональные
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    difficulty: Optional[DifficultyEnum] = None
    distance_km: Optional[float] = Field(None, ge=0.1, le=1000)
    estimated_hours: Optional[float] = Field(None, ge=0.1, le=240)


class RouteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # Pydantic V2 стиль

    id: int
    title: str
    difficulty: DifficultyEnum
    description: str
    owner_id: int


class OwnerSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str


class RouteDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    likes_count: int
    description: Optional[str]
    difficulty: DifficultyEnum
    distance_km: Optional[float]
    estimated_hours: Optional[float]
    comments: List[CommentResponse] = []
    waypoints: List[WaypointSchema] = []
    owner: OwnerSchema


# schemas.py
class RoutePreview(BaseModel):
    id: int
    title: str
    difficulty: DifficultyEnum
    distance_km: Optional[float]
    estimated_hours: Optional[float]
    likes_count: int

    model_config = ConfigDict(from_attributes=True)


class RouteListResponse(BaseModel):
    items: List[RoutePreview]
    total: int
