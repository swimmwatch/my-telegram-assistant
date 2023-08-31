"""
Data Access Layer (implementations)
"""
from services.db import models
from utils.sqlalchemy.dal import AsyncSqlAlchemyRepository
from utils.sqlalchemy.dal import SqlAlchemyRepository


class UserDAL(SqlAlchemyRepository[models.User]):
    class Config:
        model = models.User


class UserAsyncDAL(AsyncSqlAlchemyRepository[models.User]):
    class Config:
        model = models.User
