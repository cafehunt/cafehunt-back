from fastapi import APIRouter

from .cafe import router as cafe_router


api_router = APIRouter()

api_router.include_router(cafe_router, prefix="/cafes", tags=["Cafe"])
