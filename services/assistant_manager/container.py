"""
Assistant manager DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from services.assistant.config import assistant_settings
from services.assistant.grpc.client import AssistantGrpcClient


class AssistantManagerContainer(DeclarativeContainer):
    assistant_grpc_client = Singleton(
        AssistantGrpcClient,
        addr=assistant_settings.assistant_grpc_addr
    )
