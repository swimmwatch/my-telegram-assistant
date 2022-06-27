"""
Worker DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import providers
from redis import Redis

from services.assistant.grpc.client import AssistantGrpcClient
from services.sent_post_msg_info_cache_manager import SentPostMessageInfoCacheManager
from services.worker.config import ASSISTANT_GRPC_ADDR, REDIS_HOST, REDIS_PORT
from utils.post.cache.state.redis import RedisPostStateCacheManager


class WorkerContainer(DeclarativeContainer):
    assistant_grpc_client = providers.Factory(
        AssistantGrpcClient,
        addr=f'{ASSISTANT_GRPC_ADDR}'
    )
    redis_client = providers.Singleton(
        Redis,
        host=REDIS_HOST,
        port=REDIS_PORT
    )
    post_cache_state_manager = providers.Singleton(
        RedisPostStateCacheManager,
        redis_client=redis_client
    )
    sent_post_msg_info_cache_manager = providers.Singleton(
        SentPostMessageInfoCacheManager,
        redis_client=redis_client
    )
