"""
Celery worker configuration.
"""
import os

from pydantic import BaseSettings
from pydantic import RedisDsn

from services.common.config import BaseConfig

# YouTube
YT_MAX_VIDEO_LENGTH = 60 * 3
OUT_DIR = os.path.join("/tmp", "posts")  # noqa
YT_VIDEO_TTL = 60 * 2


class WorkerSettings(BaseSettings):
    celery_result_backend: RedisDsn
    celery_broker_url: RedisDsn

    class Config(BaseConfig):
        pass
