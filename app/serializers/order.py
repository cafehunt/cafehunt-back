from datetime import datetime

from pydantic import BaseModel, validator


class OrderBase(BaseModel):
    cafe_id: int
    places: int
    booking_date: str


class Order(OrderBase):
    id: int
    booking_date: datetime
    created_at: datetime
    cafe_name: str
    city_name: str
    image: str

    class Config:
        orm_mode = True


class OrderCreateResponse(OrderBase):
    booking_date: datetime

    class Config:
        orm_mode = True


class OrderCreate(OrderBase):

    class Config:
        schema_extra = {
            "example": {
                "cafe_id": 123,
                "places": 2,
                "booking_date": "2023.06.14 12"
            }
        }

        fields = {
            "cafe_id": {
                "description": "Cafe id should be more than 0"
            },
            "places": {
                "description": "Places should be more than 0"
            },
            "booking_date": {
                "description": "The booking date and hour should be in this format : YYYY.MM.DD HH"
            }
        }

    @validator("places", "cafe_id")
    def validate_places(cls, value, field):
        if value <= 0:
            raise ValueError(
                f"The value of {field.name} must be greater than 0"
            )

        return value

    @validator("booking_date")
    def validate_booking_date(cls, value):
        try:
            value = datetime.strptime(value, "%Y.%m.%d %H")
        except TypeError:
            raise ValueError(
                "Invalid booking_date format. Expected format: YYYY.MM.DD HH"
            )

        if value < datetime.now():
            raise ValueError("Booking date cannot be in the past")

        return value
