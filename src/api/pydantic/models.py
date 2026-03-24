from typing import List, Literal, Optional

from api.v1.routes.models import DifficultyEnum
from pydantic import BaseModel, Field, model_validator


def ensure_gte_zero(value: int) -> int:
    if value < 0:
        return 0
    return value


class Pagination(BaseModel):
    limit: int = Field(10, ge=4, le=50, description="Limit the number of results")
    offset: int = Field(0, ge=0, description="Смещение от начала")


class RouteFilters(Pagination):
    title: Optional[str] = Field(None, description="Поиск по подстроке")
    difficulties: Optional[List[DifficultyEnum]] = Field(
        None, description="Список сложностей"
    )
    distance_min: Optional[float] = Field(
        None, ge=0, description="Минимальное расстояние, км."
    )
    distance_max: Optional[float] = Field(
        None, ge=0, description="Максимальное расстояние, км."
    )
    duration_min: Optional[float] = Field(
        None, ge=0, description="Минимальное время, ч."
    )
    duration_max: Optional[float] = Field(
        None, ge=0, description="Максимальное время, ч."
    )

    sort_by: Optional[Literal["title", "distance", "duration", "popularity"]] = Field(
        None, description="Поле для сортировки"
    )
    order: Literal["asc", "desc"] = Field("asc", description="Направление сортировки")

    @model_validator(mode="after")
    def validate_ranges(self):
        if self.distance_min is not None and self.distance_max is not None:
            if self.distance_min > self.distance_max:
                raise ValueError("distance_min must be <= distance_max")
        if self.duration_min is not None and self.duration_max is not None:
            if self.duration_min > self.duration_max:
                raise ValueError("duration_min must be <= duration_max")
        return self
