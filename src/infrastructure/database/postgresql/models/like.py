from sqlalchemy import ForeignKey, String, Column, Integer, UniqueConstraint
from sqlalchemy.orm import  relationship, Mapped, mapped_column
from ..base import Base

class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    route_id = Column(Integer, ForeignKey("routes.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "route_id", name="uq_user_route_like"),
    )

    # Relationships
    user = relationship("User", back_populates="likes")
    route = relationship("Route", back_populates="likes")