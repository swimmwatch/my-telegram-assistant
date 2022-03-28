"""
Init Celery application.
"""
from celery import Celery

from services.worker.config import BROKER_URL, BACKEND_URL

celery = Celery(broker=BROKER_URL, backend=BACKEND_URL)
