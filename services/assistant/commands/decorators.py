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
        reply_to_message_id = request.message.reply_to_message_id
        if reply_to_message_id:
            await func(args, request)

    return wrapper
