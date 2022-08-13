"""
Assistant manager DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from services.assistant.config import assistant_settings
from services.assistant.grpc.client import AssistantGrpcClient
# from services.assistant_manager.bot import dp
# from services.assistant_manager.entrypoint import AssistantManagerEntrypoint


class AssistantManagerContainer(DeclarativeContainer):
    assistant_grpc_client = Singleton(
        AssistantGrpcClient,
        addr=assistant_settings.assistant_grpc_addr
    )
    # assistant_manager_entrypoint = Singleton(
    #     AssistantManagerEntrypoint,
    #     dp=dp
    # )
