"""
Database configuration.
"""
from pydantic import BaseSettings, SecretStr


class DatabaseSettings(BaseSettings):
    user: str = "postgres"
    password: SecretStr
    scheme: str = "postgresql+asyncpg"
    host: str = "localhost"
    name: str

    @property
    def db_url(self):
        return f"{self.scheme}://{self.user}:{self.password}@{self.host}/{self.name}"

    class Config:
        env_prefix = "db_"
