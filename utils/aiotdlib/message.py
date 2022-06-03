"""
Aiotdlib message utils.
"""
from typing import Optional

from aiotdlib.api import Message, MessageText, MessageVideo, MessageVoiceNote, MessageAnimation, MessageAudio, \
    MessageDocument, MessagePhoto
from htmgem.tags import a


def extract_text_from_telegram_message(message: Message) -> Optional[str]:
    """
    Extract text from Telegram message if it contains.

    :param message: Aiotdlib message
    :return: Message text
    """
    if isinstance(message.content, MessageText):
        formatted_text = message.content.text
    elif isinstance(message.content, MessageVideo) \
            or isinstance(message.content, MessageVoiceNote) \
            or isinstance(message.content, MessageAudio) \
            or isinstance(message.content, MessageDocument) \
            or isinstance(message.content, MessagePhoto) \
            or isinstance(message.content, MessageAnimation):
        formatted_text = message.content.caption
    else:
        return None

    return formatted_text.text


def get_mention_text(user_id: int, username: str) -> str:
    """
    Return mention text

    :param user_id: User ID
    :param username: Username
    :return: Message text with mention
    """
    return a({'href': f'tg://user?id={user_id}'}, username)
