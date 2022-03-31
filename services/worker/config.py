"""
Celery worker configuration.
"""
import os

BACKEND_URL = os.environ.get('BACKEND_URL')
BROKER_URL = os.environ.get('BROKER_URL')

# Assistant gRPC service
ASSISTANT_SERVICE_ADDR = os.environ.get('ASSISTANT_SERVICE_ADDR')
