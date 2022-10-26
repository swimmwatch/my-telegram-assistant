"""
Redis service configuration.
"""
from pydantic import BaseSettings


class RedisSettings(BaseSettings):
    host: str = 'localhost'
    port: int = 6364

    class Config:
        env_prefix = 'redis_'


redis_settings = RedisSettings()
