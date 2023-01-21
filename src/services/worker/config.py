"""
Celery worker configuration.
"""
import os

from services.assistant.config import AssistantSettings
from services.redis.config import RedisSettings

# YouTube
YT_MAX_VIDEO_LENGTH = 60 * 3
OUT_DIR = os.path.join("/tmp", "posts")
YT_VIDEO_TTL = 60 * 2


class WorkerSettings(RedisSettings, AssistantSettings):
    celery_broker_url: str = "redis://localhost:6379"
    celery_result_backend: str = "redis://localhost:6379"


worker_settings = WorkerSettings()
