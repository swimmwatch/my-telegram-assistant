"""
Command handler typings.
"""
import typing

from services.assistant.commands.request import CommandRequest

ParsedArguments = dict[str, typing.Any]
ExplicitCommandHandler = typing.Callable[[ParsedArguments, CommandRequest], typing.Awaitable[None]]
ExplicitCommandCondition = typing.Callable[[ParsedArguments], bool]
