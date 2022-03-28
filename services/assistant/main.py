import asyncio
import logging

from aiotdlib.api import API

from app.container import Container
from services.assistant import aiotdlib_client
from services.assistant.handlers import handle_new_own_message


async def main():
    aiotdlib_client.add_event_handler(handle_new_own_message, update_type=API.Types.UPDATE_NEW_MESSAGE)

    async with aiotdlib_client:
        await aiotdlib_client.idle()


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__])

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
