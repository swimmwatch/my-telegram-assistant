"""
Control panel API DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import providers

from services.db import AsyncDatabase
from services.db.config import DB_URL
from services.db.dal import UserRepository


class ControlPanelApiContainer(DeclarativeContainer):
    db = providers.Singleton(
        AsyncDatabase,
        db_url=DB_URL
    )
    user_repository = providers.Singleton(
        UserRepository,
        session_factory=db.provided.session
    )
