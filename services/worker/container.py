"""
Worker DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import providers

from services.assistant.grpc_client import AssistantGrpcClient
from services.worker.config import ASSISTANT_SERVICE_ADDR


class WorkerContainer(DeclarativeContainer):
    assistant_grpc_client = providers.Singleton(
        AssistantGrpcClient,
        addr=f'{ASSISTANT_SERVICE_ADDR}'
    )
