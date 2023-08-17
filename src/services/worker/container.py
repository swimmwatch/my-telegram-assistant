"""
Worker DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory
from dependency_injector.providers import Singleton
from redis import Redis

from services.assistant.config import AssistantSettings
from services.assistant.grpc_.client import AssistantGrpcClient
from services.post.cache.redis import RedisPostStateCache
from services.redis.config import RedisSettings
from services.worker.config import WorkerSettings

worker_settings = WorkerSettings()  # type: ignore
redis_settings = RedisSettings()  # type: ignore
assistant_settings = AssistantSettings()  # type: ignore


class WorkerContainer(DeclarativeContainer):
    assistant_grpc_client = Factory(AssistantGrpcClient, addr=assistant_settings.assistant_grpc_addr)
    redis_client = Singleton(Redis.from_url, url=redis_settings.url)
    post_cache_state: Singleton[RedisPostStateCache] = Singleton(RedisPostStateCache, redis_client=redis_client)
