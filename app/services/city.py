from sqlalchemy import select

from app.models import City
from app.repositories.city_repo import CityRepository


class CityService:

    def __init__(self, city_repo: CityRepository):
        self.repo = city_repo

    async def get_all_cities(self):
        query = select(City)

        return await self.repo.get_all(query)
