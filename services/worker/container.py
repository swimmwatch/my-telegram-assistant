"""
Worker DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import providers
from redis import Redis

from services.assistant.grpc_client import AssistantGrpcClient
from services.worker.config import ASSISTANT_GRPC_ADDR, REDIS_HOST, REDIS_PORT


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
