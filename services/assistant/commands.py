from collections import deque
from typing import NamedTuple, Type, Dict, Callable, Deque, Any, Awaitable, Optional, Tuple

from aiotdlib import Client
from aiotdlib.api import UpdateNewMessage
from loguru import logger

from utils.common.patterns import AsyncChainOfResponsibility


class CommandRequest(NamedTuple):
    """
    Command request data.
    """
    client: Client
    message: str
    update: UpdateNewMessage


ParsedArguments = Dict[str, Any]
ExplicitCommandHandler = Callable[[ParsedArguments, CommandRequest], Awaitable[None]]
ExplicitCommandCondition = Callable[[ParsedArguments], bool]


class ExplicitCommand:
    """
    Explicit command.
    """
    MAX_COMMAND_NAME_LEN = 16

    def __init__(self, name: str):
        """
        Create explicit command instance.

        :param name: Command name
        """
        if not name:
            raise ValueError('Command name must be not empty')

        if '\\' in name:
            raise ValueError(r'Command name must doesn\'t contain "\" character')

        if len(name) >= ExplicitCommand.MAX_COMMAND_NAME_LEN:
            raise ValueError(f'Command name length must be less then {ExplicitCommand.MAX_COMMAND_NAME_LEN}')

        if any(char.isdigit() for char in name):
            raise ValueError('Command name must doesn\'t contain digits')

        self._name = name
        self._args: Dict[str, Type] = {}
        self._handlers: Deque[Tuple[ExplicitCommandHandler, Optional[ExplicitCommandCondition]]] = deque()

    @property
    def name(self) -> str:
        """
        Command name property.
        """
        return self._name

    def _add_arg(self, name: str, type_: Type) -> None:
        """
        Private method for adding command argument.

        :param name: Argument name
        :param type_: Value type
        """
        self._args[name] = type_

    def add_arg(self, name: str, type_: Type) -> 'ExplicitCommand':
        """
        Add command argument.

        :param name: Argument
        :param type_: Value type
        :return: Self
        """
        self._add_arg(name, type_)
        return self

    def _add_handler(self, func: ExplicitCommandHandler, condition: Optional[ExplicitCommandCondition]) -> None:
        """
        Private method for adding explicit command handler.

        :param func: Explicit command handler
        :param condition: Explicit command condition predicate
        """
        self._handlers.append(
            (func, condition)
        )

    def on(self, condition: Optional[ExplicitCommandCondition] = None) -> Callable[[ExplicitCommandHandler], None]:
        """
        Decorate explicit command handler.

        :param condition: Explicit command condition predicate
        :return: Decorated explicit command handler that calls if condition returns True
        """
        def wrapper(func: ExplicitCommandHandler) -> None:
            self._add_handler(func, condition)

        return wrapper

    async def emit(self, args: ParsedArguments, command_request: CommandRequest) -> None:
        """
        Emit handler with passed arguments and command request.

        :param args: Parsed command arguments
        :param command_request: Command request
        """
        for func, condition in self._handlers:
            if condition:
                condition(args) and (await func(args, command_request))
            else:
                await func(args, command_request)

    def parse(self, text: str) -> Optional[ParsedArguments]:
        """
        Parse command arguments from text.

        :param text: Some text
        :return: Parsed command arguments
        """
        if not text:
            return None

        parts = text.split()
        actual_command_name = parts[0]
        expected_command_name = fr'\{self._name}'

        if not text.startswith(expected_command_name) or actual_command_name != expected_command_name:
            return None

        values = parts[1:]
        res = {arg_name: None for arg_name in self._args}
        try:
            for (arg_name, arg_type), arg_value in zip(self._args.items(), values):
                res[arg_name] = arg_type(arg_value)
        except ValueError:
            return None
        return res


class ExplicitCommandHandlerWrapper(AsyncChainOfResponsibility):
    """
    Handler wrapper for explicit commands.
    """
    def __init__(self, next_handler: Optional['AsyncChainOfResponsibility'], command: ExplicitCommand):
        super().__init__(next_handler)
        self.command = command

    async def process_request(self, request: CommandRequest) -> bool:
        """
        Process explicit command request.

        :param request: Command request
        :return: Parsing status
        """
        args = self.command.parse(request.message)

        if args is None:
            return False

        await self.command.emit(args, request)
        logger.info(f'handling {self.command.name} command')

        return True
