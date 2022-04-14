"""
Basic class for social networks posts.
"""
from abc import ABC, abstractmethod
from datetime import timedelta

from utils.aiotdlib.protocols import SupportsTelegramSending
from utils.common.patterns import Factory


class Post(ABC, SupportsTelegramSending):
    @property
    @abstractmethod
    def id(self) -> str:
        """
        :return: Post ID
        """
        pass

    @abstractmethod
    def download(self, out_dir: str) -> str:
        """Download post"""
        pass

    @property
    @abstractmethod
    def ttl(self) -> timedelta:
        """
        :return: Post TTL in cache
        """
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        """
        :return: Post title
        """
        pass

    @abstractmethod
    def clear(self, out_filename: str) -> None:
        """
        Clear post.
        """
        pass

    @staticmethod
    @abstractmethod
    def init_from_id(id_: str) -> 'Post':
        """
        Create Post instances by post_id

        :param id_: Post ID
        :return: Post instance
        """


class PostFactory(Factory):
    """
    Post factory that creates post instances by post ID.
    """
    @staticmethod
    def init_from_post_id(post_id: str) -> Post:
        class_name, id_ = post_id.split(':')
        subclasses = {class_.__name__: class_ for class_ in Post.__subclasses__()}
        return subclasses[class_name].init_from_id(id_)
