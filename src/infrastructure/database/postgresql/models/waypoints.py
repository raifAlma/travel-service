import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Float, Boolean, DateTime, ForeignKey, Enum as SQLEnum, Index

from sqlalchemy.orm import  relationship
from ..base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text

class Waypoint(Base):
    __tablename__ = "waypoints"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    #order_index: Mapped[int] = mapped_column(nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    #created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # ForeignKey к маршруту
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id", ondelete="CASCADE"))

    # Relationship
    route: Mapped["Route"] = relationship(back_populates="waypoints")

    # Индекс для быстрого поиска точек маршрута
   # __table_args__ = (
    #    Index('idx_waypoint_route_order', 'route_id', 'order_index'),
    #)