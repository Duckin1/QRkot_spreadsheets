from sqlalchemy import Column, ForeignKey, Integer, Text

from .base import BaseAbstractModel


class Donation(BaseAbstractModel):
    """Модель пожертвования"""

    user_id = Column(Integer, ForeignKey("user.id"))
    comment = Column(Text)

    def __repr__(self):
        return (
            f"user_id: {self.user_id}, " f"comment: {self.comment[:10]}, "
        ) + super().__repr__()
