"""
Telegram assistant configuration.
"""

from pydantic import BaseSettings


class AssistantSettings(BaseSettings):
    telegram_api_id: int = 0
    telegram_api_hash: str = ''
    assistant_grpc_addr: str = 'localhost:50051'

    qr_login_timeout: float = 60.0


assistant_settings = AssistantSettings()
