"""
Assistant DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import providers

from services.assistant_manager.config import assistant_manager_settings
from services.assistant_manager.grpc.client import AssistantManagerGrpcClient


class AssistantContainer(DeclarativeContainer):
    assistant_manager_grpc_client = providers.Factory(
        AssistantManagerGrpcClient,
        addr=assistant_manager_settings.assistant_manager_grpc_addr
    )
