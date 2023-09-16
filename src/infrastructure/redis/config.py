"""
Redis service configuration.
"""
from pydantic import BaseSettings

from infrastructure.common.config import BaseConfig
from infrastructure.common.config import RunLevelBaseConfigMixin


class RedisSettings(RunLevelBaseConfigMixin, BaseSettings):
    host: str
    db: int

    @property
    def url(self):
        return f"redis://{self.host}/{self.db}"

    class Config(BaseConfig):
        env_prefix = "redis_"
