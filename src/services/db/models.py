import sqlalchemy as sa
from sqlalchemy import orm

from services.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = orm.mapped_column(sa.Integer, primary_key=True)
    tg_id = orm.mapped_column(sa.Integer, unique=True, index=True)
    session = orm.mapped_column(sa.String, nullable=True, default=None)
