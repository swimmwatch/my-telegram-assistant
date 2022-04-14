"""
Celery worker configuration.
"""
import os

BACKEND_URL = os.environ.get('BACKEND_URL')
BROKER_URL = os.environ.get('BROKER_URL')

# Assistant gRPC service
ASSISTANT_GRPC_ADDR = os.environ.get('ASSISTANT_GRPC_ADDR', 'localhost')

# YouTube
YT_MAX_VIDEO_LENGTH = 60 * 3
OUT_DIR = os.path.join('/tmp', 'posts')
YT_VIDEO_TTL = 60 * 2

# Redis
REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')
