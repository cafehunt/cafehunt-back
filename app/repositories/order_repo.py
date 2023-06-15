from app.models import Order
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository):

    model = Order
