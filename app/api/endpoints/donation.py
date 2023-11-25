from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.investment import invest_to_charity_project

router = APIRouter()


@router.get(
    "/",
    response_model=list[DonationDB],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_multi(session)


@router.get(
    "/my",
    response_model=list[DonationDB],
    response_model_exclude={"fully_invested", "invested_amount", "user_id"},
)
async def get_my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    donations = await donation_crud.get_donation_by_user(
        session=session, user=user
    )
    return donations


@router.post(
    "/",
    response_model=DonationDB,
    response_model_exclude_none=True,
    response_model_exclude={"fully_invested", "invested_amount", "user_id"},
)
async def create_charity_project(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
) -> Donation:
    new_donation = await donation_crud.create(
        donation, session,
        user, is_not_committed=False
    )
    charity_projects = await charity_project_crud.get_not_fully_invested(
        session
    )
    charity_projects = invest_to_charity_project(
        new_donation, charity_projects
    )
    session.add_all(charity_projects)
    await session.commit()
    await session.refresh(new_donation)
    return new_donation
