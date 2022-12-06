"""
Common patterns.
"""
from abc import ABC, abstractmethod
from typing import Optional, Protocol


class Repository(Protocol):
    """
    Repository protocol.
    """

    pass


class Factory(Protocol):
    """Factory protocol."""

    pass


class ChainOfResponsibility(ABC):
    """Chain Of Responsibility pattern"""

    def __init__(self, next_handler: Optional["ChainOfResponsibility"]):
        self._next_handler = next_handler

    def handle(self, request):
        handled = self.process_request(request)

        if not handled and self._next_handler:
            self._next_handler.handle(request)

    @abstractmethod
    def process_request(self, request) -> bool:
        pass


class AsyncChainOfResponsibility(ABC):
    """Asynchronous Chain Of Responsibility pattern"""

    def __init__(self, next_handler: Optional["AsyncChainOfResponsibility"]):
        self._next_handler = next_handler

    async def handle(self, request):
        handled = await self.process_request(request)

        if not handled and self._next_handler:
            await self._next_handler.handle(request)

    @abstractmethod
    async def process_request(self, request) -> bool:
        pass
