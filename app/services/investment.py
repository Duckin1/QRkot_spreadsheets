from datetime import datetime as dt
from typing import Union

from app.models.base import InvestmentModel
from app.models.charity_project import CharityProject


async def invest_to_charity_project(
    source: Union[CharityProject, InvestmentModel], targets
) -> Union[CharityProject, InvestmentModel]:
    source.invested_amount = source.invested_amount or 0

    for target in targets:
        source_remaining_amount = source.full_amount - source.invested_amount
        target_remaining_amount = target.full_amount - target.invested_amount

        allocated_amount = min(source_remaining_amount, target_remaining_amount)

        for obj in (target, source):
            obj.invested_amount += allocated_amount
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested, obj.close_date = True, dt.now()

        if source.fully_invested:
            break
    return targets
