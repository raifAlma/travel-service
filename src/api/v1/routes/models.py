from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum
from api.v1.way_points import WaypointSchema
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
    #owner_name: str
    #created_at: datetime
    # НЕ включает waypoints для списков


#  Схема для детального просмотра маршрута
class RouteDetailResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: Optional[str]
    difficulty: DifficultyEnum
    distance_km: Optional[float]
    estimated_hours: Optional[float]
    created_at: datetime
    owner_id: int
    owner_name: str
    # Включаем точки маршрута
    waypoints: List[WaypointSchema] = []
