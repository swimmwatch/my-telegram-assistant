"""
Celery worker configuration.
"""
import os

from pydantic import BaseSettings

# YouTube
YT_MAX_VIDEO_LENGTH = 60 * 3
OUT_DIR = os.path.join("/tmp", "posts")  # noqa
YT_VIDEO_TTL = 60 * 2


class WorkerSettings(BaseSettings):
    celery_broker_url: str = "redis://localhost:6379"
    celery_result_backend: str = "redis://localhost:6379"
