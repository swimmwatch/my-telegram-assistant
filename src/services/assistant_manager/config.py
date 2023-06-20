"""
Assistant manager configuration.
"""
from pydantic import AnyHttpUrl
from pydantic import BaseSettings
from pydantic import SecretStr

from services.common.config import RunLevelBaseConfigMixin


class AssistantManagerSettings(RunLevelBaseConfigMixin, BaseSettings):
    my_telegram_id: int = 0
    telegram_api_token: SecretStr
    telegram_bot_webapp_url: AnyHttpUrl

    assistant_manager_grpc_addr: str
