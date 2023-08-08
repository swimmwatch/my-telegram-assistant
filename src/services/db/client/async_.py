"""
Async database client.
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from ..config import DatabaseSettings

database_settings = DatabaseSettings()  # type: ignore
async_engine = create_async_engine(database_settings.db_url, echo=database_settings.debug)
AsyncSession_ = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
