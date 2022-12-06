"""
Database service utilities.
"""
from services.db import AsyncDatabase
from services.db.models import User


async def async_init_db(db: AsyncDatabase):
    """
    Init database.
    :param db: Database
    """

    await db.init()

    async with db.session() as session:
        # init subjects
        session.add_all(User(name=name) for name in ["Dmitry", "Alex", "Drag"])

        await session.commit()
