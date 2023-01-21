"""
Data access layer.
"""
from abc import ABC
from typing import Generic, Callable, List, AsyncContextManager

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from utils.common.patterns import Repository
from utils.common.types import ContextManagerType
from services.db.models import User


class SQLAlchemyRepository(Repository, ABC, Generic[ContextManagerType]):
    """
    SQLAlchemy repository.
    """

    def __init__(self, session_factory: Callable[..., ContextManagerType]):
        self.session_factory: Callable[..., ContextManagerType] = session_factory


class UserRepository(SQLAlchemyRepository[AsyncContextManager[AsyncSession]]):
    """
    User repository that uses SQLAlchemy.
    """

    async def get_all(self) -> List[User]:
        async with self.session_factory() as session:
            async with session.begin():
                stmt = select(User)
                res = await session.execute(stmt)
                return res.scalars()
