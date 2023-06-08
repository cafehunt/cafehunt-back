from sqlalchemy import select

from app.repositories.cafe_repo import CafeRepository
from app.serializers.cafe import Cafe
from app.models.cafe import Cafe


class CafeService:

    def __init__(self, product_repo: CafeRepository):
        self.repo = product_repo

    def get_all_cafes(self):
        query = select(Cafe)
        return self.repo.get_all(query)

    async def get_cafe_by_id(self, cafe_id):
        query = select(Cafe).where(Cafe.id == cafe_id)
        return await self.repo.get_one_obj(query)