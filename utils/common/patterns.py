"""
Common patterns.
"""
from abc import ABC, abstractmethod
from typing import Protocol


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
    def __init__(self, next_handler: 'ChainOfResponsibility'):
        self._next_handler = next_handler

    def handle(self, request):
        handled = self.process_request(request)

        if not handled:
            self._next_handler.handle(request)

    @abstractmethod
    def process_request(self, request) -> bool:
        pass
