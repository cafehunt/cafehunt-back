import datetime

from fastapi import HTTPException
from sqlalchemy import select, and_, exists, func
from sqlalchemy.orm import joinedload
from starlette import status

from app.models import User, Cafe, City, Image
from app.repositories.order_repo import OrderRepository

from app.models.order import Order


class OrderService:

    def __init__(self, order_repo: OrderRepository):
        self.repo = order_repo

    async def get_user_orders(self, user: User):
        subquery_images = (
            select(Image.url)
            .where(Image.cafe_id == Cafe.id)
            .limit(1)
            .as_scalar()
        )

        query = (
            select(
                Order.id,
                Order.cafe_id,
                Order.created_at,
                Order.places,
                Order.booking_date,
                Cafe.id.label("cafe_id"),
                Cafe.name.label("cafe_name"),
                City.name.label("city_name"),
                subquery_images.label("image")
            )
            .join(Cafe, Cafe.id == Order.cafe_id)
            .join(City, City.id == Cafe.city_id)
            .where(Order.user_id == user.id)
        )

        response = await self.repo.get_all(query, scalars=False)

        return response

    async def create_order(self, data: dict):
        await self.check_order_at_this_time(data)
        await self.check_vacant_places(data)

        return await self.repo.create(data)

    async def delete_order(self, order_id: int, user: User):
        query = select(Order).where(Order.id == order_id)

        order = await self.repo.get_one_obj(query)

        if order.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN
            )

        if order.booking_date < datetime.datetime.now():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can't delete an "
                       "order that has already been processed"
            )

        return await self.repo.delete(order_id)

    async def check_order_at_this_time(self, data: dict):
        query = select(Order).where(
            and_(
                Order.user_id == data["user_id"],
                Order.booking_date == data["booking_date"]
            )
        )

        if await self.repo.exists(query):
            raise HTTPException(
                detail="Order already exists on this time",
                status_code=status.HTTP_400_BAD_REQUEST
            )

    async def check_vacant_places(self, data: dict):
        query_cafe = select(Cafe).where(Cafe.id == data["cafe_id"])

        cafe = await self.repo.get_one_obj(query_cafe)

        if cafe is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found cafe"
            )

        query = (
            select(func.sum(Order.places))
            .where(
                and_(
                    Order.cafe_id == cafe.id,
                    Order.booking_date == data["booking_date"]
                )
            )
        )

        booked_places = await self.repo.get_one_obj(query)

        if booked_places is None:
            available_places = cafe.places
        else:
            available_places = cafe.places - booked_places

        if available_places < data["places"]:
            raise HTTPException(
                detail={
                    "mes": "Not enough places",
                    "available_places": available_places
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )
