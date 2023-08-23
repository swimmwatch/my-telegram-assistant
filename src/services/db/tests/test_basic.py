import typing

import pytest

from services.db import dal
from services.db import models
from utils.factory import FactoryMaker
from utils.sqlalchemy.types import SessionFactory

user = FactoryMaker(
    models.User,
    tg_id=1,
    session="super-secret-session",
)


@pytest.fixture()
def user_repo(db_session_maker: SessionFactory) -> dal.UserDAL:
    return dal.UserDAL(db_session_maker)


# TODO: fix
# class TestUpdateOrCreate:
#     def test_not_exist(self, user_repo: dal.UserDAL) -> None:
#         assert not user_repo.all().one_or_none()
#
#         user_create_or_update = user_repo.update_or_create(tg_id=1)
#         user_create_or_update(tg_id=2)
#
#         assert user_repo.all().one_or_none()
#
#     def test_exist(self, user_repo: dal.UserDAL, db_factory: typing.Callable) -> None:
#         db_factory(user)
#
#         instance = user_repo.all().one_or_none()
#         assert instance
#         initial_pk = instance.id
#
#         user_create_or_update = user_repo.update_or_create(tg_id=1)
#         user_create_or_update(tg_id=2)
#
#         instance = user_repo.all().one_or_none()
#         assert instance
#         assert instance.tg_id == 2
#         assert initial_pk == instance.id


class TestGetOneOrMany:
    def test_first_not_exist(self, user_repo: dal.UserDAL) -> None:
        assert not user_repo.all().one_or_none()

        instance = user_repo.filter(id=1).first()
        assert not instance

    def test_first_exist(self, user_repo: dal.UserDAL, db_factory: typing.Callable) -> None:
        db_factory(user)
        assert user_repo.all().one_or_none()

        instance = user_repo.filter(tg_id=1).first()
        assert instance

    def test_all_not_exist(self, user_repo: dal.UserDAL) -> None:
        assert not user_repo.all().all()

    def test_all_exist(self, user_repo: dal.UserDAL, db_factory: typing.Callable) -> None:
        db_factory(user)
        actual = user_repo.all().all()
        assert actual
        assert len(actual) == 1


class TestCreate:
    def test_create_one(self, user_repo: dal.UserDAL) -> None:
        instance = user_repo.create_one(tg_id=1, session="my-super-session")

        assert instance.tg_id == 1
        assert instance.session == "my-super-session"

        assert user_repo.all().one_or_none() == instance


class TestDelete:
    def test_delete_one(self, user_repo: dal.UserDAL, db_factory: typing.Callable) -> None:
        db_factory(user)

        assert user_repo.all().one_or_none()

        user_repo.filter(tg_id=1).delete()

        assert not user_repo.all().one_or_none()


class TestUpdate:
    def test_update_one(self, user_repo: dal.UserDAL, db_factory: typing.Callable) -> None:
        instance: models.User = db_factory(user)

        assert user_repo.all().one_or_none()
        assert not instance.updated

        new_session = "new-secret-session"
        user_repo.filter(tg_id=1).update(session=new_session)

        instance = user_repo.all().one_or_none()
        assert instance
        assert instance.session == new_session
