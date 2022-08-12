"""
Assistant DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.wiring import providers
from telethon import TelegramClient

from services.assistant.assistant import Assistant
from services.assistant.config import assistant_settings
from services.assistant.entrypoint import AssistantEntrypoint
from services.assistant_manager.config import assistant_manager_settings
from services.assistant_manager.grpc.client import AssistantManagerGrpcClient


class AssistantContainer(DeclarativeContainer):
    telegram_client = providers.Singleton(
        TelegramClient,
        session='anon',
        api_id=assistant_settings.aiotdlib_api_id,
        api_hash=assistant_settings.aiotdlib_api_hash,
    )
    assistant_manager_grpc_client = providers.Factory(
        AssistantManagerGrpcClient,
        addr=assistant_manager_settings.assistant_manager_grpc_addr
    )
    assistant = providers.Singleton(
        Assistant,
        telegram_client=telegram_client.provided,
        assistant_manager_grpc_client=assistant_manager_grpc_client.provided
    )
    assistant_entrypoint = providers.Factory(
        AssistantEntrypoint,
        assistant=assistant.provided
    )
