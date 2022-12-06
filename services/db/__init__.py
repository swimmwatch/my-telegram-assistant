"""
Database service.
"""
from contextlib import asynccontextmanager
from typing import AsyncContextManager, ContextManager, Protocol, Union

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from services.db.types import SessionType

Base = declarative_base()
AnySessionAbstractContextManager = Union[
    ContextManager[SessionType], AsyncContextManager[SessionType]
]


class SQLAlchemyDatabaseProtocol(Protocol):
    """
    SQLAlchemy database protocol.
    """

    def session(self) -> AnySessionAbstractContextManager:
        """
        Implements method that returns SQLAlchemy session context manager.
        """
        ...

    def init(self):
        """
        Implements initialization.
        """
        ...


class AsyncDatabase(SQLAlchemyDatabaseProtocol):
    def __init__(self, db_url: str):
        """
        :param db_url: Database URL.
        """
        self._engine = create_async_engine(db_url, echo=True)
        self._session_factory = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )

    @asynccontextmanager
    async def session(self):
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception as err:
            logger.error(f"Session rollback because of exception: {err}")
            await session.rollback()
        finally:
            await session.close()

    async def init(self):
        """
        Database initialization.
        """
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
