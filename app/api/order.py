from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from starlette import status

from app.serializers.cafe import Cafe, CafeList
from app.services.cafe import CafeService
from app.utils.dependencies.services import get_cafe_service

router = APIRouter()


@router.get("", response_model=None)
async def get_user_orders():
    pass
