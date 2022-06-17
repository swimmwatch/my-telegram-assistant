"""
Database configuration.
"""

from os import environ

DB_USER = environ.get('DB_USER', 'postgres')
DB_PASSWORD = environ.get('DB_PASSWORD')
DB_NAME = environ.get('DB_NAME')
DB_HOST = environ.get('DB_HOST', 'localhost')
DB_SCHEME = 'postgresql+asyncpg'
DB_URL = f'{DB_SCHEME}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
