"""
Redis service configuration.
"""
from pydantic import BaseSettings

from services.common.config import RunLevelBaseConfigMixin


class RedisSettings(RunLevelBaseConfigMixin, BaseSettings):
    host: str = "localhost:6380"
    db: int = 0

    @property
    def url(self):
        return f"redis://{self.host}/{self.db}"

    class Config:
        env_prefix = "redis_"
