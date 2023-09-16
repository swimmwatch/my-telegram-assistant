import contextlib
import os
import typing
from collections.abc import Iterable

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import drop_database

from infrastructure.db.config import DatabaseSettings
from infrastructure.db.tests.utils import _upgrade_head
from utils.factory import FactoryType
from utils.sqlalchemy.types import AsyncSessionFactory
from utils.sqlalchemy.types import AsyncSessionGenerator


@pytest.fixture(scope="session")
def async_db_engine(request) -> typing.Generator[AsyncEngine, None, None]:
    os.environ["DB_NAME"] = "async_test"  # override default database
    settings = DatabaseSettings()

    if not database_exists(settings.url):
        create_database(settings.url)

    engine = create_async_engine(settings.url, echo=settings.debug)

    _upgrade_head(settings, request.config.rootdir)

    try:
        yield engine
    finally:
        drop_database(settings.url)


@pytest_asyncio.fixture()
async def async_db_session(async_db_engine: AsyncEngine) -> AsyncSessionGenerator:
    connection = await async_db_engine.connect()
    transaction = await connection.begin()
    test_local_session = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=connection,
        class_=AsyncSession,
    )
    session = test_local_session()

    try:
        yield session
    finally:
        await session.close()
        await transaction.rollback()  # rollback to the savepoint
        await connection.close()


@pytest.fixture()
def async_db_session_maker(async_db_session: AsyncSession) -> AsyncSessionFactory:
    @contextlib.asynccontextmanager
    async def session_maker() -> AsyncSessionGenerator:
        yield async_db_session

    return session_maker


@pytest.fixture()
def async_instance(async_db_session: AsyncSession) -> typing.Callable:
    """
    SQLAlchemy model instance factory.

    :param async_db_session: SQLAlchemy session
    :return: Model instance
    """

    async def make(*args):
        async_db_session.add_all(args)
        await async_db_session.commit()
        return args

    return make


@pytest.fixture()
def async_db_factory(async_instance: typing.Callable) -> typing.Callable:
    """
    Uses FactoryMaker for creating database instances.
    """

    async def make(factory_maker: FactoryType | None):
        if factory_maker is None:
            return

        data = factory_maker.make()
        if isinstance(data, Iterable):
            return await async_instance(*data)
        else:
            obj = await async_instance(data)
            return obj[0]

    return make
