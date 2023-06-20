from typing import Type, Generic, Optional, TypeVar

import sqlalchemy as sa
from sqlalchemy.orm import Session

T = TypeVar("T")


class SqlAlchemyRepository(Generic[T]):
    class Config:
        model: Type

    def __init__(self, session: Session):
        self.session = session

    def get_one_or_none(self, **kwargs) -> Optional[T]:
        stmt = sa.select(self.Config.model).filter_by(**kwargs)
        res = self.session.execute(stmt).scalar_one_or_none()
        return res
