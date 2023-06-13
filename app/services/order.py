from app.repositories.order_repo import OrderRepository


class OrderService:

    def __init__(self, order_repo: OrderRepository):
        self.repo = order_repo
