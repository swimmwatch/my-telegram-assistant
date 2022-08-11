"""
Command decorators.
"""
import functools

from services.assistant.commands import ExplicitCommandHandler, ParsedArguments, CommandRequest


def serve_only_replied_request(func: ExplicitCommandHandler) -> ExplicitCommandHandler:
    """
    Decorate explicit command handler for handling only replied requests.

    :param func: Explicit command handler
    :return: Wrapped explicit command handler
    """
    @functools.wraps(func)
    async def wrapper(args: ParsedArguments, request: CommandRequest):
        if request.event.is_reply:
            await func(args, request)

    return wrapper


def serve_only_basic_group_messages(func: ExplicitCommandHandler) -> ExplicitCommandHandler:
    """
    Decorate explicit command handler for handling messages only from basic chat.

    :param func: Explicit command handler
    :return: Wrapped explicit command handler
    """
    @functools.wraps(func)
    async def wrapper(args: ParsedArguments, request: CommandRequest):
        chat_info = await request.client.get_chat_info(request.message.chat_id, full=True)
        if isinstance(chat_info, BasicGroupFullInfo):
            await func(args, request)

    return wrapper
