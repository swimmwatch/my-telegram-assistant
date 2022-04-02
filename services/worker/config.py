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
YT_OUT_DIR = os.path.join('/tmp', 'youtube')
YT_VIDEO_TTL = 60 * 2
