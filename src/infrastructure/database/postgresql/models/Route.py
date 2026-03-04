import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Text, Float, Boolean, DateTime, ForeignKey, Enum as SQLEnum

from sqlalchemy.orm import  relationship
from ..base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text
class DifficultyEnum(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"

class Route(Base):
    __tablename__ = "routes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    difficulty: Mapped[DifficultyEnum] = mapped_column(
        SQLEnum(DifficultyEnum),
        default=DifficultyEnum.MEDIUM
    )

    distance_km: Mapped[Optional[float]] = mapped_column(Float)
    estimated_hours: Mapped[Optional[float]] = mapped_column(Float)
    #created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # ForeignKey к пользователю
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    #owner_name: Mapped[str] = mapped_column(ForeignKey("users.username", ondelete="CASCADE"), nullable=False)


    # Relationships
    owner: Mapped["User"] = relationship(back_populates="routes", foreign_keys=[owner_id])
    waypoints: Mapped[List["Waypoint"]] = relationship(
        back_populates="route",
        cascade="all, delete-orphan",

    )
    