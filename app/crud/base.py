from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class CRUDBase:
    def __init__(self, model) -> None:
        self.model = model

    async def get(
        self,
        obj_id,
        session: AsyncSession,
    ):
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return db_obj.scalars().first()

    async def get_multi(
        self,
        session: AsyncSession,
    ):
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in,
        session: AsyncSession,
        user: Optional[User] = None,
        do_commit: bool = True,
    ):
        new_obj_data = obj_in.dict()
        if user is not None:
            new_obj_data["user_id"] = user.id
        if new_obj_data.get('invested_amount') is None:
            new_obj_data['invested_amount'] = 0
        db_obj = self.model(**new_obj_data)
        session.add(db_obj)
        if do_commit:
            await session.commit()
            await session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj, obj_in, session: AsyncSession):
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(self, db_obj, session: AsyncSession):
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_not_fully_invested(
        self,
        session: AsyncSession,
    ):
        objects = await session.execute(
            select(self.model)
            .order_by(self.model.create_date)
            .where(self.model.fully_invested == 0)
        )
        objects = objects.scalars().all()
        return objects
