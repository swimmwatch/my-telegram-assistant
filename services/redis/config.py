"""
Redis service configuration.
"""
from pydantic import BaseSettings


class RedisSettings(BaseSettings):
    redis_host: str = 'localhost'
    redis_port: int = 6364


redis_settings = RedisSettings()
