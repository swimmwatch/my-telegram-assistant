from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from services.assistant_manager.config import assistant_manager_settings

bot = Bot(assistant_manager_settings.telegram_api_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
