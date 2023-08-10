"""
Database configuration.
"""
from pydantic import BaseSettings

from services.common.config import RunLevelBaseConfigMixin


class DatabaseSettings(RunLevelBaseConfigMixin, BaseSettings):
    user: str = "postgres"
    password: str = "mypass"
    scheme: str = "postgresql+psycopg"
    host: str = "localhost:5555"
    name: str = "my_telegram_assistant"
    debug: bool = True

    @property
    def url(self):
        return f"{self.scheme}://{self.user}:{self.password}@{self.host}/{self.name}"

    class Config:
        env_prefix = "db_"
