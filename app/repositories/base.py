from typing import Any

from sqlalchemy import insert, delete, update
from sqlalchemy.sql import Select


class BaseRepository:

    model: Any = None

    def __init__(self, session):
        self.session = session

    async def create(self, new_obj: dict):
        query = insert(self.model).returning(self.model)

        response = await self.session.execute(query, new_obj)
        await self.session.commit()
        result = response.scalar()

        return result

    async def get_all(self, query: Select, scalars: bool = True):
        response = await self.session.execute(query)

        result = response.unique().scalars().all() if scalars else response.all()

        return result

    async def get_one_obj(self, query: Select, scalar: bool = True):
        response = await self.session.execute(query)

        result = response.scalar() if scalar else response

        return result

    async def update(
            self,
            data: dict,
            pk: Any,
            *filters,
            pk_name: str = "id",
            in_session: bool = False
    ):
        query = (
            update(self.model)
            .where(getattr(self.model, pk_name) == pk, *filters)
            .returning(self.model)
        )

        response = await self.session.execute(query, data)

        if not in_session:
            await self.session.commit()

        result = response.one()

        return result

    async def delete(self, obj_id: int):
        query = delete(self.model).where(self.model.id == obj_id)

        await self.session.execute(query)
        await self.session.commit()

    async def exists(self, query: Select):
        query = query.with_only_columns(self.model.id)
        response = await self.session.execute(query)
        result = response.first()

        return bool(result)
