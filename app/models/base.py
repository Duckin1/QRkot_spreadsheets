from datetime import datetime as dt

import sqlalchemy as sa
from sqlalchemy import Boolean, Column, DateTime, Integer

from app.core.db import Base


class BaseAbstractModel(Base):
    """Абстрактный класс для моделей CharityProject и Donation"""

    __abstract__ = True

    __table_args__ = (
        sa.CheckConstraint("full_amount > 0", name="full_amount is not positive"),
        sa.CheckConstraint("invested_amount >= 0", name="invested_amount is negative"),
        sa.CheckConstraint(
            "invested_amount <= full_amount",
            name="invested_amount is more than full_amount",
        ),
    )

    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=dt.now)
    close_date = Column(DateTime, default=None)

    def __repr__(self):
        return (
            f"full_amount: {self.full_amount}, "
            f"invested_amount: {self.invested_amount}, "
            f"create_date: {self.create_date}"
        )
