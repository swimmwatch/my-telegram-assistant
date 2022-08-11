"""
Telegram assistant configuration.
"""

from pydantic import BaseSettings


class AssistantSettings(BaseSettings):
    aiotdlib_api_id: int = 0
    aiotdlib_api_hash: str = ''
    phone_number: str = ''
    assistant_grpc_addr: str = 'localhost:50051'

    assistant_qr_login_timeout: float = 60.0


assistant_settings = AssistantSettings()
