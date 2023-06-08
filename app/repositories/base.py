from typing import Any

from sqlalchemy import insert, delete, update
from sqlalchemy.sql import Select


class BaseRepository:

    model: Any = None

    def __init__(self, session):
        self.session = session

    def create(self, new_obj: dict):
        query = insert(self.model).returning(self.model)

        response = self.session.execute(query, new_obj)
        self.session.commit()
        result = response.scalar()

        return result

    def get_all(self, query: Select, scalars: bool = True):
        response = self.session.execute(query)

        result = response.scalars().all() if scalars else response.all()

        return result

    def get_one_obj(self, query: Select, scalar: bool = True):
        response = self.session.execute(query)

        result = response.scalar() if scalar else response

        return result

    def update(
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

        response = self.session.execute(query, data)

        if not in_session:
            self.session.commit()

        result = response.one()

        return result

    def delete(self, obj_id: int):
        query = delete(self.model).where(self.model.id == obj_id)

        self.session.execute(query)
        self.session.commit()
