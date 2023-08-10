"""
SQLAlchemy Data Access Layer.
"""
import typing

import sqlalchemy as sa
from sqlalchemy import inspect

from utils.sqlalchemy.types import SessionFactory

T = typing.TypeVar("T")


class SqlAlchemyRepository(typing.Generic[T]):
    class Config:
        # TODO: annotate using generic
        model: typing.Type

    def __init__(self, session_factory: SessionFactory):
        self.session_factory = session_factory
        self._base_query = sa.select(self.Config.model)

    def base(self, query: sa.Select) -> "SqlAlchemyRepository":
        self._base_query = query
        return self

    def query(self) -> sa.Select:
        return self._base_query

    def filter(self, **kwargs) -> "SqlAlchemyRepository":
        self._base_query = self._base_query.filter_by(**kwargs)
        return self

    def where(self, *args) -> "SqlAlchemyRepository":
        self._base_query = self._base_query.where(*args)
        return self

    def order_by(self, *args) -> "SqlAlchemyRepository":
        self._base_query = self._base_query.order_by(*args)
        return self

    def group_by(self, *args) -> "SqlAlchemyRepository":
        self._base_query = self._base_query.group_by(*args)
        return self

    def join(self, *args) -> "SqlAlchemyRepository":
        self._base_query = self._base_query.join(*args)
        return self

    def first(self) -> T | None:
        with self.session_factory() as session:
            return session.execute(self._base_query).scalar_one_or_none()

    def all(self) -> sa.ScalarResult[T]:
        with self.session_factory() as session:
            return session.execute(self._base_query).scalars()

    @property
    def pk(self) -> str | None:
        meta = inspect(self.Config.model)
        if not meta:
            return None

        return meta.primary_key[0].name

    def create_one(self, **kwargs):
        with self.session_factory() as session:
            instance = self.Config.model(**kwargs)
            session.add(instance)
            session.commit()
            return instance

    @classmethod
    def _update(cls, instance, **kwargs):
        for key, value in kwargs.items():
            setattr(instance, key, value)
        return instance

    def update_instance(self, instance, **kwargs):
        with self.session_factory() as session:
            updated_instance = self._update(instance, **kwargs)
            session.commit()
            return updated_instance

    def update_or_create(self, **kwargs) -> typing.Callable:
        def update(**inner_kwargs):
            instance = self.filter(**kwargs).first()

            if not instance:
                params = {**kwargs, **inner_kwargs}
                if self.pk and self.pk in params:
                    params.pop(self.pk)
                return self.create_one(**params)

            instance = self.update_instance(instance, **inner_kwargs)

            return instance

        return update
