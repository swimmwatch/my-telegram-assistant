"""
Assistant manager configuration.
"""
from pathlib import Path

from pydantic import AnyHttpUrl
from pydantic import BaseSettings
from pydantic import SecretStr

from services.common.config import BaseConfig
from services.common.config import RunLevelBaseConfigMixin

BASE_DIR = Path(__file__).resolve().parent


class TelegramBotSettings(RunLevelBaseConfigMixin, BaseSettings):
    token: SecretStr
    webapp_url: AnyHttpUrl

    grpc_addr: str

    template_dir: Path = BASE_DIR / "templates"

    class Config(BaseConfig):
        env_prefix = "telegram_bot_"
