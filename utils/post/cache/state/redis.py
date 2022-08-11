from os import PathLike
from typing import Tuple

from redis import Redis

from utils.post.cache.state import PostCacheState, SupportsPostStateCache


class RedisPostStateCacheManager(SupportsPostStateCache):
    """
    Implementation of post cache manager for Redis.
    """

    STATE_KEY_PATTERN = 'state:%s'
    STATE_VALUE_SEP = '\t'

    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def get_state(self, post_id: str) -> Tuple[PostCacheState, PathLike | None]:
        key = self.STATE_KEY_PATTERN % post_id
        state_str = self.redis_client.get(key)
        if not state_str:
            return PostCacheState.NONE, None

        dec_state_str = state_str.decode()
        state, output_filename = dec_state_str.split(self.STATE_VALUE_SEP)
        return PostCacheState[state], output_filename or None

    def set_state(self, post_id: str, new_state: PostCacheState, out_filename: str = '') -> None:
        key = self.STATE_KEY_PATTERN % post_id
        val = f'{new_state.value}{self.STATE_VALUE_SEP}{out_filename}'
        self.redis_client.set(key, val)

    def clear_state(self, post_id: str):
        key = self.STATE_KEY_PATTERN % post_id
        self.redis_client.delete(key)
