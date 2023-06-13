from fastapi import APIRouter

from .cafe import router as cafe_router
from .order import router as order_router


api_router = APIRouter()

api_router.include_router(cafe_router, prefix="/cafes", tags=["Cafe"])

api_router.include_router(order_router, prefix="/orders", tags=["Order"])
