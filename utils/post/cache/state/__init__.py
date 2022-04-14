"""
Post cache state manager.
"""
from enum import Enum
from typing import Protocol


class PostCacheState(Enum):
    """
    Post cache states.
    """
    NONE = 'NONE'
    DOWNLOADED = 'DOWNLOADED'
    DOWNLOADING = 'DOWNLOADING'


class SupportsPostStateCache(Protocol):
    """
    Protocol that declares getting and setting cache state.
    """
    def get_state(self, post_id: str) -> PostCacheState:
        """
        Get post cache state.

        :param post_id: Post ID
        :return: Post state
        """
        ...

    def set_state(self, post_id: str, new_state: PostCacheState) -> None:
        """
        Set post cache state.

        :param post_id: Post ID
        :param new_state: New state
        """
        ...

    def clear_state(self, post_id: str) -> None:
        """
        Clear post cache state.

        :param post_id:
        :return:
        """
        ...
