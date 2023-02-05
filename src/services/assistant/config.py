"""
Telegram assistant configuration.
"""

from pydantic import BaseSettings, SecretStr


class AssistantSettings(BaseSettings):
    telegram_api_id: SecretStr
    telegram_api_hash: SecretStr
    assistant_grpc_addr: str = "localhost:50051"

    qr_login_timeout: float = 60.0
