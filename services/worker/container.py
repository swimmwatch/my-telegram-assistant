"""
Worker DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import providers
from redis import Redis

from services.assistant.grpc.client import AssistantGrpcClient
from services.worker.config import worker_settings
from utils.post.cache.state.redis import RedisPostStateCacheManager


class WorkerContainer(DeclarativeContainer):
    assistant_grpc_client = providers.Factory(
        AssistantGrpcClient,
        addr=worker_settings.grpc_addr
    )
    redis_client = providers.Singleton(
        Redis,
        host=worker_settings.redis_host,
        port=worker_settings.redis_port
    )
    post_cache_state_manager = providers.Singleton(
        RedisPostStateCacheManager,
        redis_client=redis_client
    )
