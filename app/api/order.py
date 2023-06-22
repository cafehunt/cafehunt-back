from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import Field

from app.api.user import fastapi_users

from app.models import User
from app.services.order import OrderService
from app.serializers.order import OrderCreate, Order, OrderCreateResponse
from app.utils.dependencies.services import get_order_service
from fastapi_pagination import Page, paginate

router = APIRouter()

Page = Page.with_custom_options(
    size=Field(5, ge=1, le=20),
    page=Field(1, ge=1)
)


@router.get("", response_model=Page[Order])
async def get_user_orders(
        user: User = Depends(fastapi_users.current_user()),
        service: OrderService = Depends(get_order_service)
):
    orders = await service.get_user_orders(user=user)

    return paginate(orders)


@router.post("", response_model=OrderCreateResponse)
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
