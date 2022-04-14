"""
Common custom typings.
"""
from contextlib import AbstractContextManager, AbstractAsyncContextManager
from typing import TypeVar

# Context manager
ContextManagerType = TypeVar('ContextManagerType', AbstractContextManager, AbstractAsyncContextManager)
