"""
Database configuration.
"""
from pydantic import BaseSettings
from pydantic import SecretStr

from services.common.config import BaseConfig
from services.common.config import RunLevelBaseConfigMixin


class DatabaseSettings(RunLevelBaseConfigMixin, BaseSettings):
    user: str
    password: SecretStr
    scheme: str = "postgresql+psycopg"
    host: str
    name: str
    debug: bool = True

    @property
    def url(self):
        """
        Returns database URL.
        """
        password = self.password.get_secret_value()
        return f"{self.scheme}://{self.user}:{password}@{self.host}/{self.name}"

    class Config(BaseConfig):
        env_prefix = "db_"
