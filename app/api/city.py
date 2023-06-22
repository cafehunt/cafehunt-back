from fastapi import APIRouter, Depends

from app.serializers.city import City
from app.services.city import CityService
from app.utils.dependencies.services import get_city_service

router = APIRouter()


@router.get("", response_model=list[City])
async def get_all_cities(
        service: CityService = Depends(get_city_service)
):
    return await service.get_all_cities()
