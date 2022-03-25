"""
Celery worker configuration.
"""
import os

BACKEND_URL = os.environ.get('BACKEND_URL')
BROKER_URL = os.environ.get('BROKER_URL')
