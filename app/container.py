"""
Main DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import providers
from redis import Redis

from app.config import REDIS_HOST, REDIS_PORT


class Container(DeclarativeContainer):
    redis_client = providers.Singleton(
        Redis,
        host=REDIS_HOST,
        port=REDIS_PORT
    )
