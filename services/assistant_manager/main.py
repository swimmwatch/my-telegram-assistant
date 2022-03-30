from aiogram.types import Message
from aiogram.utils import executor
from dependency_injector.wiring import inject, Provide
from loguru import logger
from redis import Redis

from app.config import MY_TELEGRAM_ID
from app.container import Container
from services.assistant_manager.bot import dp
from utils.aiogram.decorators import serve_only_specific_user

serve_only_me = serve_only_specific_user(MY_TELEGRAM_ID)


@dp.message_handler(regexp=r'^[0-9]+$')
@serve_only_me
@inject
async def handle_getting_auth_code(msg: Message, redis_client: Redis = Provide[Container.redis_client]):
    code = msg.text
    logger.info(f'got auth code: {code}')  # TODO: remove from logs auth code
    redis_client.set('auth_code', code)


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__])

    logger.info('launch bot')
    executor.start_polling(dp)
