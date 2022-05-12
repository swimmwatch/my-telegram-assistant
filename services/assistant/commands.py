from collections import deque
from typing import NamedTuple, Type, Dict, Callable, Deque, Any, Awaitable, Optional

from aiotdlib import Client


class CommandRequest(NamedTuple):
    client: Client
    message: str
    chat_id: int


ParsedArguments = Dict[str, Any]
ExplicitCommandHandler = Callable[[ParsedArguments, Client, CommandRequest], Awaitable[None]]


class ExplicitCommand:
    def __init__(self, name: str):
        self._name = name
        self._args: Dict[str, Type] = {}
        self._handlers: Deque[ExplicitCommandHandler] = deque()

    def _add_arg(self, name: str, type_: Type):
        self._args[name] = type_

    def add_arg(self, name: str, type_: Type):
        self._add_arg(name, type_)
        return self

    def _add_handler(self, func: ExplicitCommandHandler):
        self._handlers.append(func)

    def on(self, func: ExplicitCommandHandler) -> None:
        self._add_handler(func)

    async def emit(self, args: ParsedArguments, client: Client, command_request: CommandRequest):
        for handler in self._handlers:
            await handler(args, client, command_request)

    def parse(self, text: str) -> Optional[ParsedArguments]:
        # TODO: write unittests
        parts = text.split()
        actual_command_name = parts[0]
        expected_command_name = fr'\{self._name}'

        if not text.startswith(expected_command_name) and actual_command_name == expected_command_name:
            return None

        values = parts[1:]
        return {arg_name: arg_type(val) for (arg_name, arg_type), val in zip(self._args.items(), values)}
