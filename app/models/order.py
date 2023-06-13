__all__ = ["Order", "OrderTime"]

from sqlalchemy import Column, Integer, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base


class OrderTime(Base):
    __tablename__ = "order_times"

    id = Column(Integer, primary_key=True)
    date = Column(Date)
    hour = Column(Integer)
    order_id = Column(Integer, ForeignKey('order.id'))

    order = relationship("Order", back_populates="order_times")


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    places = Column(Integer)
    user_id = Column(Integer, ForeignKey("user.id"))
    created_at = Column(DateTime)

    order_times = relationship("OrderTime", back_populates="order")
