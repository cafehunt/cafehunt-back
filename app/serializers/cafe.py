from datetime import time

from pydantic import BaseModel

from app.models import AverageBill


class ImageBase(BaseModel):
    url: str

    class Config:
        orm_mode = True


class CafeBase(BaseModel):
    name: str


class CafeList(CafeBase):
    id: int
    street: str
    places: int
    images: list[ImageBase] = []
    rating: float
    reviews: int
    average_bill: AverageBill
    is_favourite_cafe: bool = False
    work_time_start: time
    work_time_end: time
    has_wifi: bool
    has_coworking_place: bool
    can_with_pets: bool
    has_outdoor_seating: bool
    has_vegan_menu: bool

    class Config:
        orm_mode = True


class Cafe(CafeList):
    phone_number: str | None


class VacantPlaces(BaseModel):
    cafe_id: int
    available_places: int

    class Config:
        orm_mode = True
