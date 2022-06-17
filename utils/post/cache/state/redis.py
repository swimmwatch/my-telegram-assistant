from redis import Redis

from utils.post.cache.state import PostCacheState, SupportsPostStateCache


class RedisPostStateCacheManager(SupportsPostStateCache):
    """
    Implementation of post cache manager for Redis.
    """

    STATE_KEY_PATTERN = 'state:%s'

    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def get_state(self, post_id: str) -> PostCacheState:
        key = self.STATE_KEY_PATTERN % post_id
        state_str = self.redis_client.get(key)
        if not state_str:
            return PostCacheState.NONE

        dec_state_str = state_str.decode()
        return PostCacheState[dec_state_str]

    def set_state(self, post_id: str, new_state: PostCacheState) -> None:
        key = self.STATE_KEY_PATTERN % post_id
        self.redis_client.set(key, new_state.value)

    def clear_state(self, post_id: str):
        key = self.STATE_KEY_PATTERN % post_id
        self.redis_client.delete(key)
