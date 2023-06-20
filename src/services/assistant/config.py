"""
Telegram assistant configuration.
"""

from pydantic import BaseSettings
from pydantic import SecretStr

from services.common.config import RunLevelBaseConfigMixin


class AssistantSettings(RunLevelBaseConfigMixin, BaseSettings):
    telegram_api_id: SecretStr
    telegram_api_hash: SecretStr
    assistant_grpc_addr: str = "localhost:50051"

    qr_login_timeout: float = 60.0
