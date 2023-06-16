from fastapi import APIRouter
from fastapi.params import Depends
from app.api.user import fastapi_users

from app.models import User
from app.services.order import OrderService
from app.serializers.order import OrderCreate, Order, OrderBase
from app.utils.dependencies.services import get_order_service

router = APIRouter()


@router.get("", response_model=list[Order])
async def get_user_orders(
        user: User = Depends(fastapi_users.current_user()),
        service: OrderService = Depends(get_order_service)
):
    return await service.get_user_orders(user=user)


@router.post("", response_model=OrderBase)
async def create_order(
        order_data: OrderCreate,
        user: User = Depends(fastapi_users.current_user()),
        service: OrderService = Depends(get_order_service)
):
    order_data_dict = order_data.dict()
    order_data_dict["user_id"] = user.id

    return await service.create_order(data=order_data_dict)


@router.delete("/{order_id}/")
async def delete_order(
        order_id: int,
        user: User = Depends(fastapi_users.current_user()),
        service: OrderService = Depends(get_order_service)
):
    return await service.delete_order(order_id, user)
