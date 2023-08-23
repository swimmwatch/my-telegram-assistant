import contextlib
import os
import typing
from collections.abc import Iterable

import pytest
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy_utils import create_database
from sqlalchemy_utils import database_exists
from sqlalchemy_utils import drop_database

from services.db.config import DatabaseSettings
from services.db.tests.utils import _upgrade_head
from utils.factory import FactoryType
from utils.sqlalchemy.types import SessionFactory
from utils.sqlalchemy.types import SessionGenerator


@pytest.fixture(scope="session")
def db_engine(request) -> typing.Generator[sa.Engine, None, None]:
    os.environ["DB_NAME"] = "test"  # override default database
    settings = DatabaseSettings()

    if not database_exists(settings.url):
        create_database(settings.url)

    engine = sa.create_engine(settings.url, echo=settings.debug)

    _upgrade_head(settings, request.config.rootdir)

    try:
        yield engine
    finally:
        drop_database(settings.url)


@pytest.fixture()
def alembic_engine(db_engine: sa.Engine) -> sa.Engine:
    """
    Override "alembic_engine" fixture of "pytest-alembic" package.

    Check: https://pytest-alembic.readthedocs.io/en/latest/api.html#pytest_alembic.plugin.fixtures.alembic_engine

    :param db_engine: SQLAlchemy Engine instance
    :return: SQLAlchemy Engine instance
    """
    return db_engine


@pytest.fixture()
def db_session(db_engine: sa.Engine) -> SessionGenerator:
    connection = db_engine.connect()
    transaction = connection.begin()
    test_local_session = orm.sessionmaker(
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
        bind=connection,
        class_=orm.Session,
    )
    session = test_local_session()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()  # rollback to the savepoint
        connection.close()


@pytest.fixture()
def db_session_maker(db_session: orm.Session) -> SessionFactory:
    def session_maker() -> SessionGenerator:
        yield db_session

    return contextlib.contextmanager(session_maker)


@pytest.fixture()
def instance(db_session: orm.Session) -> typing.Callable:
    """
    SQLAlchemy model instance factory.

    :param db_session: SQLAlchemy session
    :return: Model instance
    """

    def make(*args):
        db_session.add_all(args)
        db_session.commit()
        return args

    return make


@pytest.fixture()
def db_factory(instance: typing.Callable) -> typing.Callable:
    """
    Uses FactoryMaker for creating database instances.
    """

    def make(factory_maker: FactoryType | None):
        if factory_maker is None:
            return

        data = factory_maker.make()
        if isinstance(data, Iterable):
            return instance(*data)
        else:
            obj = instance(data)
            return obj[0]

    return make
