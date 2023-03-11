"""
Async database client.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from ..config import DatabaseSettings

database_settings = DatabaseSettings()
async_engine = create_async_engine(database_settings.db_url, echo=database_settings.debug)
AsyncSession_ = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)
