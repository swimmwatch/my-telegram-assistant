from aiogram.types import Message
from aiogram.utils import executor
from loguru import logger

from services.assistant_manager.bot import dp


@dp.message_handler()
async def handle_any_message(msg: Message):
    await msg.reply(msg.text)


if __name__ == '__main__':
    logger.info('launch bot')
    executor.start_polling(dp)
