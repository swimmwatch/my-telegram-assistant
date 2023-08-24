from services.db.client.async_ import AsyncDatabase
from services.db.config import DatabaseSettings


def get_async_db() -> AsyncDatabase:
    settings = DatabaseSettings()
    db = AsyncDatabase(settings.url)
    return db
