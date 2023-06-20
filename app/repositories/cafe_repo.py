from app.models import Cafe, FavouriteCafe
from app.repositories.base import BaseRepository


class CafeRepository(BaseRepository):

    model = Cafe


class FavouriteCafeRepository(BaseRepository):

    model = FavouriteCafe
