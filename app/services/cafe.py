import random
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload, subqueryload
from starlette import status
from starlette.responses import Response

from app.models import Order, AverageBill, Image
from app.repositories.cafe_repo import CafeRepository, FavouriteCafeRepository
from app.serializers.cafe import Cafe

from app.models import Cafe, User, FavouriteCafe


class CafeService:

    def __init__(self, cafe_repo: CafeRepository):
        self.repo = cafe_repo

    async def get_all_cafes(
            self,
            user: User | None,
            city_id: int | None = None,
            rating: int | None = None,
            average_bill: AverageBill | None = None,
            has_wifi: bool | None = None,
            has_coworking_place: bool | None = None,
            can_with_pets: bool | None = None,
            has_outdoor_seating: bool | None = None,
            has_vegan_menu: bool | None = None,
            name: str | None = None,
            sort_by: str | None = None
    ):
        query = (
            select(Cafe).join(Cafe.images)
            .options(joinedload(Cafe.images))
        )
        filters = []

        if rating is not None and (rating < 1 or rating > 5):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Rating must be an integer between 1 and 5."
            )

        if city_id:
            filters.append(Cafe.city_id == city_id)
        if rating:
            filters.append(and_(Cafe.rating > rating - 1, Cafe.rating <= rating))
        if average_bill:
            filters.append(Cafe.average_bill == AverageBill[average_bill.upper()])
        if has_wifi:
            filters.append(Cafe.has_wifi == has_wifi)
        if has_coworking_place:
            filters.append(Cafe.has_coworking_place == has_coworking_place)
        if can_with_pets:
            filters.append(Cafe.can_with_pets == can_with_pets)
        if has_outdoor_seating:
            filters.append(Cafe.has_outdoor_seating == has_outdoor_seating)
        if has_vegan_menu:
            filters.append(Cafe.has_vegan_menu == has_vegan_menu)
        if name:
            filters.append(func.lower(Cafe.name).ilike(f"%{name.lower()}%"))

        if filters:
            query = query.where(and_(*filters))

        cafes = await self.repo.get_all(query)

        if sort_by:
            if sort_by == "rating":
                cafes.sort(key=lambda cafe: cafe.rating, reverse=True)
            elif sort_by == "average_bill":
                cafes.sort(key=lambda cafe: cafe.average_bill.sort_order)

        if user is not None:
            fav_cafe_query = select(
                FavouriteCafe.cafe_id
            ).where(FavouriteCafe.user_id == user.id)

            fav_cafes = await self.repo.get_all(fav_cafe_query)

            for cafe in cafes:
                if cafe.id in fav_cafes:
                    setattr(cafe, "is_favourite_cafe", True)

        return cafes

    async def get_cafe_by_id(
            self,
            cafe_id: int,
            user: User | None,
            with_images: bool = True
    ):
        query = select(Cafe).where(Cafe.id == cafe_id)

        if with_images:
            query = query.options(joinedload(Cafe.images))

        cafe = await self.repo.get_one_obj(query)

        if user is not None:
            fav_cafe_query = (
                select(FavouriteCafe).where(
                    and_(
                        FavouriteCafe.cafe_id == cafe_id,
                        FavouriteCafe.user_id == user.id
                    )
                )
            )

            if await self.repo.exists(fav_cafe_query):
                setattr(cafe, "is_favourite_cafe", True)

        return cafe

    async def get_random_cafes(self, amount: int = 4):
        cafes_count_query = select(func.count()).select_from(Cafe)

        cafes_count = await self.repo.get_one_obj(cafes_count_query)

        random_cafe_ids = random.sample(range(1, cafes_count + 1), amount)

        query = (
            select(Cafe).join(Cafe.images)
            .options(joinedload(Cafe.images))
            .where(Cafe.id.in_(random_cafe_ids))
        )

        return await self.repo.get_all(query)

    async def get_vacant_places(self, cafe_id: int, date: str, user: User):
        cafe = await self.get_cafe_by_id(cafe_id, user, with_images=False)

        if cafe is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not found cafe"
            )

        date = await self.validate_date(date)

        subquery = (
            select(func.sum(Order.places))
            .where(
                and_(
                    Order.cafe_id == cafe_id,
                    Order.booking_date == date
                )
            )
            .as_scalar()
        )

        query = select(
                    Cafe.id.label("cafe_id"),
                    (Cafe.places - func.coalesce(subquery, 0))
                    .label("available_places")
            )

        response = await self.repo.get_one_obj(query, scalar=False)

        result = response.fetchone()

        return result

    @staticmethod
    async def validate_date(date: str) -> datetime | HTTPException:
        try:
            date = datetime.strptime(date, "%Y.%m.%d %H")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid date format. Expected format: YYYY.MM.DD HH"
            )

        if datetime.now() > date:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Booking date cannot be in the past"
            )

        return date


class FavouriteCafeService:

    def __init__(self, fav_cafe_repo: FavouriteCafeRepository):
        self.repo = fav_cafe_repo

    async def get_favourite_cafes(self, user: User):
        subquery_fav = select(
            FavouriteCafe.cafe_id
        ).where(FavouriteCafe.user_id == user.id).subquery()

        subquery_images = (
            select(Image.url)
            .where(Image.cafe_id == Cafe.id)
            .limit(1)
            .as_scalar()
        )

        query = (
            select(
                Cafe.name,
                Cafe.street,
                Cafe.work_time_start,
                Cafe.work_time_end,
                Cafe.rating,
                Cafe.reviews,
                subquery_images.label("image")
            )
            .join(FavouriteCafe.cafe)
            .where(Cafe.id.in_(subquery_fav))
            .group_by(Cafe.id)
        )

        return await self.repo.get_all(query, scalars=False)

    async def add_or_delete_favourite(self, cafe_id, user: User):
        find_fav_query = select(FavouriteCafe).where(and_(
            FavouriteCafe.user_id == user.id,
            FavouriteCafe.cafe_id == cafe_id
        ))

        fav_cafe = await self.repo.get_one_obj(find_fav_query)

        if fav_cafe:
            await self.repo.delete(fav_cafe.id)

            return Response(status_code=204)

        fav_cafe_data = {
            "cafe_id": cafe_id,
            "user_id": user.id
        }

        fav_cafe = await self.repo.create(fav_cafe_data)

        if fav_cafe:
            return Response(status_code=201)
