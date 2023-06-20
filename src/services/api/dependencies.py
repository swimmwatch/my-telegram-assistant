"""
API dependencies.
"""
from services.db.client.async_ import AsyncSession_
from services.db.client.sync import Session_


def get_db():
    session = Session_()
    try:
        yield session
    finally:
        session.close()


async def get_async_db():
    session = AsyncSession_()
    try:
        yield session
    finally:
        await session.close()
