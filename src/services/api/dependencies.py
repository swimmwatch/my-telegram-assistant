"""
API dependencies.
"""
from services.db.client.async_ import AsyncDatabase
from services.db.client.sync import Database
from services.db.config import DatabaseSettings


def get_db():
    # TODO: add return typing
    settings = DatabaseSettings()
    return Database(settings.url).session


async def get_async_db():
    # TODO: add return typing
    settings = DatabaseSettings()
    return AsyncDatabase(settings.url).session
