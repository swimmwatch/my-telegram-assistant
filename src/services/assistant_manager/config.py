"""
Assistant manager configuration.
"""
from pydantic import BaseSettings, SecretStr, AnyHttpUrl


class AssistantManagerSettings(BaseSettings):
    my_telegram_id: int = 0
    telegram_api_token: SecretStr
    telegram_bot_webapp_url: AnyHttpUrl

    assistant_manager_grpc_addr: str
