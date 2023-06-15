from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status

from app.api.user import fastapi_users
from app.models import User
from app.serializers.cafe import Cafe, CafeList, VacantPlaces
from app.services.cafe import CafeService
from app.utils.dependencies.services import get_cafe_service

router = APIRouter()


@router.get("", response_model=list[CafeList])
async def get_cafes(
        service: CafeService = Depends(get_cafe_service)
):
    return await service.get_all_cafes()


@router.get("/{cafe_id}/", response_model=Cafe)
async def get_cafes_by_id(
        cafe_id: int,
        service: CafeService = Depends(get_cafe_service)
):
    cafe = await service.get_cafe_by_id(cafe_id)

    if cafe is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found cafe"
        )

    return cafe


@router.get("/{cafe_id}/places/", response_model=VacantPlaces)
async def get_vacant_places(
        cafe_id: int,
        date: str,
        user: User = Depends(fastapi_users.current_user()),
        service: CafeService = Depends(get_cafe_service)
):
    return await service.get_vacant_places(cafe_id, date)
