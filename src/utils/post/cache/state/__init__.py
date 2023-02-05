"""
Post cache state manager.
"""
from enum import Enum
from os import PathLike
from typing import Protocol, Tuple


class PostCacheState(Enum):
    """
    Post cache states.
    """

    NONE = "NONE"
    DOWNLOADED = "DOWNLOADED"
    DOWNLOADING = "DOWNLOADING"


class SupportsPostStateCache(Protocol):
    """
    Protocol that declares getting and setting cache state.
    """

    def get_state(self, post_id: str) -> Tuple[PostCacheState, PathLike | None]:
        """
        Get post cache state.

        :param post_id: Post ID
        :return: Post state
        """
        ...

    def set_state(self, post_id: str, new_state: PostCacheState, out_filename: PathLike) -> None:
        """
        Set post cache state.

        :param post_id: Post ID
        :param new_state: New state
        :param out_filename: Output filename
        """
        ...

    def clear_state(self, post_id: str) -> None:
        """
        Clear post cache state.

        :param post_id:
        :return:
        """
        ...
