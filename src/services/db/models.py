from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from services.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
