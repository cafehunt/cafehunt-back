from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload

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

    async def get_cafe_by_id(self, cafe_id):
        query = (
            select(Cafe).join(Cafe.images)
            .options(joinedload(Cafe.images))
            .where(Cafe.id == cafe_id)
        )

        return await self.repo.get_one_obj(query)

    async def get_vacant_places(self, cafe_id: int, date: str):
        query = select(
            Cafe.id,
            (Cafe.places - func.coalesce(func.sum(Order.places), 0))
            .label("available_places")
        ).join(Order).where(
            and_(
                Order.cafe_id == cafe_id,
                Order.booking_date == date
            )
        )

        return await self.repo.get_one_obj(query)
