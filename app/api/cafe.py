from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import Field
from starlette import status

from app.api.user import fastapi_users
from app.models import User
from app.serializers.cafe import Cafe, CafeList, VacantPlaces
from app.services.cafe import CafeService, FavouriteCafeService
from app.utils.dependencies.services import (
    get_cafe_service,
    get_favourite_cafe_service
)
from fastapi_pagination import Page, paginate


router = APIRouter()


Page = Page.with_custom_options(
    size=Field(10, ge=1, le=100),
    page=Field(1, ge=1)
)


@router.get("", response_model=Page[CafeList])
async def get_cafes(
    city_id: Optional[int] = None,
    rating: Optional[int] = None,
    average_bill: Optional[str] = None,
    has_wifi: Optional[bool] = None,
    has_coworking_place: Optional[bool] = None,
    can_with_pets: Optional[bool] = None,
    has_outdoor_seating: Optional[bool] = None,
    has_vegan_menu: Optional[bool] = None,
    name: Optional[str] = None,
    service: CafeService = Depends(get_cafe_service)
):
    result = await service.get_all_cafes(
        city_id=city_id,
        rating=rating,
        average_bill=average_bill,
        has_wifi=has_wifi,
        has_coworking_place=has_coworking_place,
        can_with_pets=can_with_pets,
        has_outdoor_seating=has_outdoor_seating,
        has_vegan_menu=has_vegan_menu,
        name=name
    )

    return paginate(result)


@router.get("/explore_new/", response_model=list[CafeList])
async def get_random_cafes(
    service: CafeService = Depends(get_cafe_service)
):
    return await service.get_random_cafes()


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


@router.post("/{cafe_id}/add_to_favourite/")
async def add_to_favourite(
        cafe_id: int,
        user: User = Depends(fastapi_users.current_user()),
        service: FavouriteCafeService = Depends(get_favourite_cafe_service)
):
    return await service.add_to_favourite(cafe_id, user)


@router.get("/favourite/")
async def get_fav_cafes(
        user: User = Depends(fastapi_users.current_user()),
        service: FavouriteCafeService = Depends(get_favourite_cafe_service)
):
    return await service.get_favourite_cafes(user)


@router.delete("/favourite/{favourite_id}/")
async def delete_favourite(
        favourite_cafe_id: int,
        user: User = Depends(fastapi_users.current_user()),
        service: FavouriteCafeService = Depends(get_favourite_cafe_service)
):
    return await service.delete_favourite_cafe(favourite_cafe_id, user)
