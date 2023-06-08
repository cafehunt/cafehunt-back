from fastapi import APIRouter
from fastapi.params import Depends

from app.serializers.cafe import Cafe
from app.services.cafe import CafeService
from app.utils.dependencies.services import get_cafe_service

router = APIRouter()


@router.get("", response_model=list[Cafe])
async def get_cafes(
        service: CafeService = Depends(get_cafe_service)
):
    return await service.get_all_cafes()


@router.get("/{cafe_Id}", response_model=Cafe)
async def get_cafes_by_id(
        cafe_id: int,
        service: CafeService = Depends(get_cafe_service)
):
    return await service.get_cafe_by_id(cafe_id)
