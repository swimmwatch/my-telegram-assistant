"""
Custom typings for DB package.
"""
from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

SessionType = TypeVar('SessionType', AsyncSession, Session)
