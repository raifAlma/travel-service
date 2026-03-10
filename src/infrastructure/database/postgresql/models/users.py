from sqlalchemy.orm import  relationship, Mapped, mapped_column
from infrastructure.database.postgresql.models.Comment import Comments
from ..base import Base
from sqlalchemy import Integer, String

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(128), unique=True,  nullable=False)
    email: Mapped[str] = mapped_column(String(256), unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    tokens: Mapped[list['Token']] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # NEW: One-to-Many: пользователь создает маршруты
    routes: Mapped[list["Route"]] = relationship(
        back_populates="owner",
        cascade="all, delete-orphan",
        foreign_keys = "[Route.owner_id]"
    )



    # NEW: One-to-Many: пользователь пишет отзывы
    comments: Mapped[list["Comments"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )
"""
    # NEW: Many-to-Many: пользователь лайкает отзывы
    liked_reviews: Mapped[list["Review"]] = relationship(
        secondary="likes",  # Укажем таблицу позже
        back_populates="liked_by"
    )

"""
