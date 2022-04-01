from aiotdlib import Client
from aiotdlib.api import UpdateNewMessage
from loguru import logger

from services.worker.app import download_and_send_youtube_video
from utils.aiotdlib.decorators import serve_only_own_actions
from utils.youtube import extract_link


@serve_only_own_actions
async def handle_new_own_message(_: Client, update: UpdateNewMessage):
    chat_id = update.message.chat_id
    msg = update.message.content.text.text
    link = extract_link(msg)
    if not link:
        return

    download_and_send_youtube_video.delay(chat_id, link)
    logger.info(f'downloading link: {link}')
