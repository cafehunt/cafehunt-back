from datetime import datetime
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload
from starlette import status

from app.models import Order
from app.repositories.cafe_repo import CafeRepository
from app.serializers.cafe import Cafe
from app.models.cafe import Cafe, AverageBill


class CafeService:

    def __init__(self, cafe_repo: CafeRepository):
        self.repo = cafe_repo

    async def get_all_cafes(
            self,
            city_id: int = None,
            rating: Optional[int] = None,
            average_bill: Optional[AverageBill] = None,
            has_wifi: bool = None,
            has_coworking_place: bool = None,
            can_with_pets: bool = None,
            has_outdoor_seating: bool = None,
            has_vegan_menu: bool = None,
            name: str = None
    ):
        query = (
            select(Cafe).join(Cafe.images)
            .options(joinedload(Cafe.images))
        )

        filters = []

        if rating is not None and (rating < 1 or rating > 5):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rating must be an integer between 1 and 5."
            )

        if city_id:
            filters.append(Cafe.city_id == city_id)
        if rating:
            filters.append(and_(Cafe.rating > rating - 1, Cafe.rating <= rating))
        if average_bill:
            filters.append(Cafe.average_bill == AverageBill[average_bill.upper()])
        if has_wifi is not None:
            filters.append(Cafe.has_wifi == has_wifi)
        if has_coworking_place is not None:
            filters.append(Cafe.has_coworking_place == has_coworking_place)
        if can_with_pets is not None:
            filters.append(Cafe.can_with_pets == can_with_pets)
        if has_outdoor_seating is not None:
            filters.append(Cafe.has_outdoor_seating == has_outdoor_seating)
        if has_vegan_menu is not None:
            filters.append(Cafe.has_vegan_menu == has_vegan_menu)
        if name:
            filters.append(func.lower(Cafe.name).ilike(f"%{name.lower()}%"))

        if filters:
            query = query.where(and_(*filters))

        return await self.repo.get_all(query)

    async def get_cafe_by_id(self, cafe_id: int, with_images: bool = True):
        query = select(Cafe).where(Cafe.id == cafe_id)

        if with_images:
            query = query.options(joinedload(Cafe.images))

        return await self.repo.get_one_obj(query)

    async def get_vacant_places(self, cafe_id: int, date: str):
        cafe = await self.get_cafe_by_id(cafe_id, with_images=False)

        if cafe is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found cafe"
            )

        date = await self.validate_date(date)

        query = (
            select(func.sum(Order.places))
            .where(
                and_(
                    Order.cafe_id == cafe_id,
                    Order.booking_date == date  # Change it after moving to PostgreSQL
                )
            )
        )

        booked_places = await self.repo.get_one_obj(query)

        if booked_places is None:
            available_places = cafe.places
        else:
            available_places = cafe.places - booked_places

        return {"cafe_id": cafe_id, "available_places": available_places}

    @staticmethod
    async def validate_date(date: str) -> datetime | HTTPException:
        try:
            date = datetime.strptime(date, "%Y.%m.%d %H")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Expected format: YYYY.MM.DD HH"
            )

        if datetime.now() > date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking date cannot be in the past"
            )

        return date
