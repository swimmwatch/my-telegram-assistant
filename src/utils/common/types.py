"""
Common custom typings.
"""
from contextlib import AbstractAsyncContextManager, AbstractContextManager
from typing import TypeVar

# Context manager
ContextManagerType = TypeVar("ContextManagerType", AbstractContextManager, AbstractAsyncContextManager)
