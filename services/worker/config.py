"""
Celery worker configuration.
"""
import os

CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379')

# Assistant gRPC service
ASSISTANT_GRPC_ADDR = os.environ.get('ASSISTANT_GRPC_ADDR', 'localhost')

# YouTube
YT_MAX_VIDEO_LENGTH = 60 * 3
OUT_DIR = os.path.join('/tmp', 'posts')
YT_VIDEO_TTL = 60 * 2

# Redis
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
