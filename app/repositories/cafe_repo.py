from app.models import Cafe
from app.repositories.base import BaseRepository


class CafeRepository(BaseRepository):

    model = Cafe
