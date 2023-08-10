"""
SQLAlchemy typing utilities.
"""
import typing

from sqlalchemy import orm

SessionFactory = typing.Callable[..., typing.ContextManager[orm.Session]]
SessionGenerator = typing.Generator[orm.Session, None, None]
