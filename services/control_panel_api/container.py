"""
Control panel API DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import providers

from services.db import AsyncDatabase
from services.db.config import database_settings
from services.db.dal import UserRepository


class ControlPanelApiContainer(DeclarativeContainer):
    db = providers.Singleton(AsyncDatabase, db_url=database_settings.db_url)
    user_repo = providers.Singleton(UserRepository, session_factory=db.provided.session)
