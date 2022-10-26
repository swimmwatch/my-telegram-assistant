"""
Assistant manager configuration.
"""
from pydantic import BaseSettings


class AssistantManagerSettings(BaseSettings):
    my_telegram_id: int = 0
    telegram_api_token: str = ''

    grpc_addr: str


assistant_manager_settings = AssistantManagerSettings()
