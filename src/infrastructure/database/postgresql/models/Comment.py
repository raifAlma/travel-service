from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..base import Base


class Comments(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    comment_text: Mapped[str] = mapped_column(String(50))
    route_id: Mapped[int] = mapped_column(ForeignKey("routes.id", ondelete="CASCADE"))
    # comment_date: Mapped[datetime] = mapped_column(DateTime)
    user: Mapped["User"] = relationship(back_populates="comments")
    route: Mapped["Route"] = relationship(back_populates="comments")
