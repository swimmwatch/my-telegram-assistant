from typing import Optional

from redis import Redis

from utils.aiotdlib.models import MessageInfo
from utils.post.impl import Post


class SentPostMessageInfoCacheManager:
    REDIS_CACHED_MSG_KEY = 'cached_msg:%s'

    def __init__(self, redis_client: Redis):
        self.redis_client = redis_client

    def cache_msg_info(self, chat_id: int, message_id: int, post: Post):
        key = self.REDIS_CACHED_MSG_KEY % post.id
        message_info = MessageInfo(chat_id, message_id)
        self.redis_client.set(key, str(message_info))

    def get_msg_info(self, post: Post) -> Optional[MessageInfo]:
        key = self.REDIS_CACHED_MSG_KEY % post.id
        enc_msg_info = self.redis_client.get(key)
        if not enc_msg_info:
            return None
        msg_info_str = enc_msg_info.decode()
        msg_info = MessageInfo.from_str(msg_info_str)
        return msg_info

    def clear_msg_info(self, post: Post) -> None:
        key = self.REDIS_CACHED_MSG_KEY % post.id
        self.redis_client.delete(key)
