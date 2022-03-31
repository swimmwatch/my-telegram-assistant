from aiotdlib import Client
from aiotdlib.api import UpdateNewMessage
from loguru import logger

from services.worker.app import download_and_send_youtube_video
from utils.youtube import extract_link


async def handle_new_own_message(client: Client, update: UpdateNewMessage):
    own_id = await client.get_my_id()
    chat_id = update.message.chat_id
    sender_id = update.message.sender_id.user_id

    # handle only own messages that was sent anyone
    if own_id != sender_id:
        return

    msg = update.message.content.text.text
    link = extract_link(msg)
    if not link:
        return

    download_and_send_youtube_video.delay(chat_id, link)
    logger.info(f'downloading link: {link}')
