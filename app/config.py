"""
Application configuration.
"""

import os

REDIS_HOST = os.environ.get('REDIS_HOST')
REDIS_PORT = os.environ.get('REDIS_PORT')

MY_TELEGRAM_ID = int(os.environ.get('MY_TELEGRAM_ID'))
