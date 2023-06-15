from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.cafe_repo import CafeRepository
from app.repositories.order_repo import OrderRepository
from app.services.cafe import CafeService
from app.services.order import OrderService
from app.utils.dependencies.get_session import get_session


def get_cafe_service(
        session: AsyncSession = Depends(get_session)
) -> CafeService:
    repo = CafeRepository(session)
    service = CafeService(cafe_repo=repo)

    return service


def get_order_service(
        session: AsyncSession = Depends(get_session)
) -> OrderService:
    repo = OrderRepository(session)
    service = OrderService(order_repo=repo)

    return service
