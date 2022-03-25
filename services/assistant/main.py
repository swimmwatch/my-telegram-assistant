import asyncio
import logging
import re

from aiotdlib import Client
from aiotdlib.api import API, UpdateNewMessage

from services.assistant.config import AIOTDLIB_API_ID, AIOTDLIB_API_HASH, PHONE_NUMBER

INST_POST_MATCH = re.compile(r'https://www.instagram.com/p/.+/')


async def handle_new_own_message(client: Client, update: UpdateNewMessage):
    sender_id = update.message.sender_id.user_id
    own_id = await client.get_my_id()

    # handle only own messages that was sent anyone
    if own_id != sender_id:
        return

    message = update.message.content.text.text
    match = INST_POST_MATCH.search(message)
    if not match:
        return

    link = match.group(0)
    logging.info(f'sending link: {link}')


async def main():
    client = Client(
        api_id=AIOTDLIB_API_ID,
        api_hash=AIOTDLIB_API_HASH,
        phone_number=PHONE_NUMBER,
    )

    client.add_event_handler(handle_new_own_message, update_type=API.Types.UPDATE_NEW_MESSAGE)

    async with client:
        await client.idle()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
