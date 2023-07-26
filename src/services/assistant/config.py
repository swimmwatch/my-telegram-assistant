"""
Telegram assistant configuration.
"""
from pathlib import Path

from pydantic import BaseSettings
from pydantic import SecretStr

from services.common.config import RunLevelBaseConfigMixin


BASE_DIR = Path(__file__).resolve().parent


class AssistantSettings(RunLevelBaseConfigMixin, BaseSettings):
    telegram_api_id: SecretStr
    telegram_api_hash: SecretStr
    assistant_grpc_addr: str = "localhost:50051"
    template_dir: Path = BASE_DIR / "templates"

    qr_login_timeout: float = 60.0
