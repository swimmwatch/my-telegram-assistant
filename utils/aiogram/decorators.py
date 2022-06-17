import functools
from typing import Callable

from aiogram.types import Message


def serve_only_specific_user(user_id: int) -> Callable:
    """
    Decorates Aiogram handler for serving only specific user messages.
    :param user_id: Telegram user ID
    :return: Decorated handler
    """
    def decorator(handler: Callable) -> Callable:
        @functools.wraps(handler)
        async def wrapper(message: Message, *args, **kwargs) -> None:
            sender_id = message.from_user.id
            if sender_id == user_id:
                await handler(message, *args, **kwargs)
        return wrapper
    return decorator
