from aiotdlib import Client
from aiotdlib.api import UpdateNewMessage, MessageText
from loguru import logger

from services.worker.app import download_and_send_post
from utils.aiotdlib.decorators import serve_only_own_actions
from utils.youtube import extract_link


@serve_only_own_actions
async def handle_new_own_message(_: Client, update: UpdateNewMessage):
    chat_id = update.message.chat_id

    content = update.message.content
    if not isinstance(content, MessageText):
        return

    formatted_text = content.text
    msg = formatted_text.text
    link = extract_link(msg)
    if not link:
        return

    download_and_send_post.delay(chat_id, link)
    logger.info(f'downloading post: {link}')
