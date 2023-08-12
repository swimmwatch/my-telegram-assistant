import typing

import pytest

from services.db import dal
from services.db import models
from utils.factory import FactoryMaker
from utils.sqlalchemy.types import AsyncSessionFactory

user = FactoryMaker(
    models.User,
    tg_id=1,
    session="super-secret-session",
)


@pytest.fixture()
def user_repo(async_db_session_maker: AsyncSessionFactory) -> dal.UserAsyncDAL:
    return dal.UserAsyncDAL(async_db_session_maker)


# TODO: fix
# @pytest.mark.asyncio()
# class TestUpdateOrCreate:
#     async def test_not_exist(self, user_repo: dal.UserAsyncDAL) -> None:
#         result = await user_repo.all()
#         assert not result.one_or_none()
#
#         user_create_or_update = user_repo.update_or_create(tg_id=1)
#         await user_create_or_update(tg_id=2)
#
#         result = await user_repo.all()
#         assert result.one_or_none()
#
#     async def test_exist(self, user_repo: dal.UserAsyncDAL, async_db_factory: typing.Callable) -> None:
#         await async_db_factory(user)
#
#         result = await user_repo.all()
#         instance = result.one_or_none()
#         assert instance
#         initial_pk = instance.id
#
#         user_create_or_update = user_repo.update_or_create(tg_id=1)
#         await user_create_or_update(tg_id=2)
#
#         result = await user_repo.all()
#         instance = result.one_or_none()
#         assert instance
#         assert instance.tg_id == 2
#         assert initial_pk == instance.id


@pytest.mark.asyncio()
class TestGetOneOrMany:
    async def test_first_not_exist(self, user_repo: dal.UserAsyncDAL) -> None:
        instance = await user_repo.all()
        assert not instance.one_or_none()

        instance = await user_repo.filter(id=1).first()
        assert not instance

    async def test_first_exist(self, user_repo: dal.UserAsyncDAL, async_db_factory: typing.Callable) -> None:
        await async_db_factory(user)
        instance = await user_repo.all()
        assert instance.one_or_none()

        instance = await user_repo.filter(tg_id=1).first()
        assert instance

    async def test_all_not_exist(self, user_repo: dal.UserAsyncDAL) -> None:
        actual = await user_repo.all()
        assert not actual.all()

    async def test_all_exist(self, user_repo: dal.UserAsyncDAL, async_db_factory: typing.Callable) -> None:
        await async_db_factory(user)
        result = await user_repo.all()
        actual = result.all()
        assert actual
        assert len(actual) == 1


@pytest.mark.asyncio()
class TestCreate:
    async def test_create_one(self, user_repo: dal.UserAsyncDAL) -> None:
        instance = await user_repo.create_one(tg_id=1, session="my-super-session")

        assert instance.tg_id == 1
        assert instance.session == "my-super-session"

        result = await user_repo.all()
        assert result.one_or_none() == instance


@pytest.mark.asyncio()
class TestDelete:
    async def test_delete_one(self, user_repo: dal.UserAsyncDAL, async_db_factory: typing.Callable) -> None:
        await async_db_factory(user)

        result = await user_repo.all()
        assert result.one_or_none()

        await user_repo.filter(tg_id=1).delete()

        result = await user_repo.all()
        assert not result.one_or_none()