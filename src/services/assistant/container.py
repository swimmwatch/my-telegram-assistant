"""
Assistant DI container.
"""
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton
from telethon import TelegramClient
from telethon.sessions import MemorySession

from services.assistant.assistant import Assistant
from services.assistant.config import AssistantSettings
from services.assistant.entrypoint import AssistantEntrypoint
from services.assistant_manager.config import AssistantManagerSettings
from services.assistant_manager.grpc.client import AssistantManagerGrpcClient
from services.redis.config import RedisSettings

assistant_manager_settings = AssistantManagerSettings()
assistant_settings = AssistantSettings()
redis_settings = RedisSettings()


class AssistantContainer(DeclarativeContainer):
    telegram_client: Singleton[TelegramClient] = Singleton(
        TelegramClient,
        session=MemorySession(),
        api_id=assistant_settings.telegram_api_id.get_secret_value(),
        api_hash=assistant_settings.telegram_api_hash.get_secret_value(),
    )
    assistant_manager_grpc_client = Singleton(
        AssistantManagerGrpcClient,
        addr=assistant_manager_settings.assistant_manager_grpc_addr,
    )
    assistant = Singleton(
        Assistant,
        telegram_client=telegram_client.provided,
        assistant_manager_grpc_client=assistant_manager_grpc_client.provided,
    )
    assistant_entrypoint = Factory(AssistantEntrypoint, assistant=assistant.provided)
