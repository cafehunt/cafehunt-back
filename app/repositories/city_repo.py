from app.models import City
from app.repositories.base import BaseRepository


class CityRepository(BaseRepository):

    model = City
