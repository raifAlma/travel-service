from infrastructure.database.postgresql.models.Comment import Comments
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    tokens: Mapped[list["Token"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # NEW: One-to-Many: пользователь создает маршруты
    routes: Mapped[list["Route"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
        foreign_keys="[Route.owner_id]",
    )

    # NEW: One-to-Many: пользователь пишет отзывы
    comments: Mapped[list["Comments"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    likes = relationship("Likes", back_populates="user", cascade="all, delete-orphan")
