from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum

class WaypointSchema(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    #order_index: int = Field(..., ge=0)
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    route_id: int


class WaypointUpdate(BaseModel):
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


