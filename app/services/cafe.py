from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload
from starlette import status

from app.models import Order
from app.repositories.cafe_repo import CafeRepository
from app.serializers.cafe import Cafe
from app.models.cafe import Cafe


class CafeService:

    def __init__(self, cafe_repo: CafeRepository):
        self.repo = cafe_repo

    async def get_all_cafes(self):
        query = (
            select(Cafe).join(Cafe.images)
            .options(joinedload(Cafe.images))
        )
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

        subquery = (
            select(func.sum(Order.places))
            .where(
                and_(
                    Order.cafe_id == cafe_id,
                    Order.booking_date == date
                )
            )
            .as_scalar()
        )

        query = select(
                    Cafe.id.label("cafe_id"),
                    (Cafe.places - func.coalesce(subquery, 0))
                    .label("available_places")
            )

        response = await self.repo.get_one_obj(query, scalar=False)

        result = response.fetchone()

        return result

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
