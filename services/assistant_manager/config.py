"""
Assistant manager configuration.
"""
import os

# Telegram
from pydantic import BaseSettings

TELEGRAM_API_TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
MY_TELEGRAM_ID = int(os.environ.get('MY_TELEGRAM_ID', 0))


class AssistantManagerSettings(BaseSettings):
    my_telegram_id: int = 0
    telegram_api_token: str


assistant_manager_settings = AssistantManagerSettings()
