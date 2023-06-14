__all__ = ["Order"]

from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    places = Column(Integer, default=1)
    user_id = Column(Integer, ForeignKey("user.id"))
    cafe_id = Column(Integer, ForeignKey("cafe.id"))
    booking_date = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now())

    cafe = relationship("Cafe", back_populates="orders")
    user = relationship("User", back_populates="orders")
