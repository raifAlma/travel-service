import enum
from typing import Optional, List
from sqlalchemy import Float, ForeignKey, Enum as SQLEnum, Integer, String, Text
from sqlalchemy.orm import  relationship, Mapped, mapped_column

from ..base import Base

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

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    comments: Mapped[list['Comments']] = relationship(back_populates="route", cascade="all, delete-orphan")



    owner: Mapped["User"] = relationship(back_populates="routes", foreign_keys=[owner_id])
    waypoints: Mapped[List["Waypoint"]] = relationship(
        back_populates="route",
        cascade="all, delete-orphan",

    )
    