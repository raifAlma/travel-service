from typing import Optional

from sqlalchemy import Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class Waypoint(Base):
    __tablename__ = "waypoints"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    title: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(String(500))
    # created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id", ondelete="CASCADE"))

    route: Mapped["Route"] = relationship(back_populates="waypoints")
