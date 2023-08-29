"""
Assistant DI container.
"""
from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from services.assistant.client import AssistantClient
from services.assistant.config import AssistantSettings
from services.assistant.entrypoint import AssistantEntrypoint
from services.bot.config import TelegramBotSettings
from services.bot.grpc_.client import TelegramBotAsyncGrpcClient
from services.db.client.async_ import AsyncDatabase
from services.db.config import DatabaseSettings


class AssistantContainer(DeclarativeContainer):
    database_config = DatabaseSettings()
    telegram_bot_config = TelegramBotSettings()
    assistant_config = AssistantSettings()

    bot_grpc_client = providers.Singleton(
        TelegramBotAsyncGrpcClient,
        addr=telegram_bot_config.grpc_addr,
    )
    async_database = providers.Singleton(
        AsyncDatabase,
        db_url=database_config.url,
    )
    assistant = providers.Singleton(
        AssistantClient,
        api_id=assistant_config.api_id.get_secret_value(),
        api_hash=assistant_config.api_hash.get_secret_value(),
    )
    assistant_entrypoint = providers.Factory(
        AssistantEntrypoint,
        grpc_addr=assistant_config.grpc_addr,
        assistant_client=assistant.provided,
        bot_grpc_client=bot_grpc_client.provided,
        session_factory=async_database.provided.session,
    )
