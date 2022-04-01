"""
Aiotdlib decorators.
"""
import functools
from typing import Callable

import aiotdlib
from aiotdlib.api import UpdateNewMessage


def serve_only_own_actions(handler: Callable) -> Callable:
    """
    Decorates Aiotdlib handler for serving only own actions.
    :return: Decorated handler
    """
    @functools.wraps(handler)
    async def wrapper(client: aiotdlib.Client, update: UpdateNewMessage, *args, **kwargs) -> None:
        own_id = await client.get_my_id()
        sender_id = update.message.sender_id.user_id
        if own_id == sender_id:
            await handler(client, update, *args, **kwargs)
    return wrapper
