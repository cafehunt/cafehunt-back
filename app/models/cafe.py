__all__ = ["Cafe", "City", "Image", "AverageBill"]

from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Enum as EnumType,
    BOOLEAN,
    Float,
    Time
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class AverageBill(Enum):
    CHEAP = "$"
    MIDDLE = "$$"
    EXPENSIVE = "$$$"


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String(63))

    cafes = relationship("Cafe", back_populates="city")


class Cafe(Base):
    __tablename__ = "cafe"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    city_id = Column(Integer, ForeignKey("city.id"))
    street = Column(String)
    places = Column(Integer)
    average_bill = Column(EnumType(AverageBill), default=AverageBill.MIDDLE)
    rating = Column(Float, default=0)
    reviews = Column(Integer, default=0)
    work_time_start = Column(Time)
    work_time_end = Column(Time)
    has_wifi = Column(BOOLEAN, default=False)
    has_coworking_place = Column(BOOLEAN, default=False)
    can_with_pets = Column(BOOLEAN, default=False)
    has_outdoor_seating = Column(BOOLEAN, default=False)
    has_vegan_menu = Column(BOOLEAN, default=False)

    city = relationship("City", back_populates="cafes")
    images = relationship("Image", back_populates="cafe")
    orders = relationship("Order", back_populates="cafe")


class Image(Base):
    __tablename__ = "image"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    cafe_id = Column(Integer, ForeignKey("cafe.id"))

    cafe = relationship("Cafe", back_populates="images")
