from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_charity_project_by_name(
        self, charity_project_name: str, session: AsyncSession
    ) -> Optional[int]:
        db_charity_project_id = await session.execute(
            select(CharityProject.id).where(CharityProject.name == charity_project_name)
        )
        db_charity_project_id = db_charity_project_id.scalars().first()
        return db_charity_project_id

    async def get_all_fully_invested_project(
        self,
        session: AsyncSession,
    ) -> List[CharityProject]:
        closed_projects = await session.execute(
            select(
                [
                    CharityProject.name,
                    CharityProject.create_date,
                    CharityProject.close_date,
                    CharityProject.description,
                ]
            ).where(CharityProject.fully_invested == True)
        )
        return closed_projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
