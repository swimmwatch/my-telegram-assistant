"""
Worker DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton
from redis import Redis

from services.assistant.config import AssistantSettings
from services.assistant.grpc.client import AssistantGrpcClient
from services.redis.config import RedisSettings
from services.worker.config import WorkerSettings
from utils.post.cache.state.redis import RedisPostStateCacheManager

worker_settings = WorkerSettings()  # type: ignore
redis_settings = RedisSettings()  # type: ignore
assistant_settings = AssistantSettings()  # type: ignore


class WorkerContainer(DeclarativeContainer):
    assistant_grpc_client = Factory(AssistantGrpcClient, addr=assistant_settings.assistant_grpc_addr)
    redis_client = Singleton(Redis, host=redis_settings.host, port=redis_settings.port)
    post_cache_state_manager = Singleton(RedisPostStateCacheManager, redis_client=redis_client)
