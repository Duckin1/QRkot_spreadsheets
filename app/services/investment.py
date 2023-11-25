from datetime import datetime as dt
from typing import List

from app.models.base import InvestmentModel


async def invest_to_charity_project(
    source: InvestmentModel,
    targets: List[InvestmentModel],
) -> List[InvestmentModel]:
    modified = []
    for target in targets:

        amount = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )

        for obj in (target, source):
            obj.invested_amount += amount
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested, obj.close_date = True, dt.now()
        modified.append(source)
        if target.fully_invested:
            break
    return modified
