from fastapi import APIRouter

from .cafe import router as cafe_router
from .order import router as order_router
from .user import router as user_router
from .city import router as city_router


api_router = APIRouter(prefix="/api")

api_router.include_router(cafe_router, prefix="/cafes", tags=["Cafe"])

api_router.include_router(order_router, prefix="/orders", tags=["Order"])

api_router.include_router(city_router, prefix="/cities", tags=["City"])

api_router.include_router(user_router)
