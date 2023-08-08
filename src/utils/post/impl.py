"""
Basic class for social networks posts.
"""
import os
from abc import ABC
from abc import abstractmethod
from datetime import timedelta
from os import path

import pytube
from pytube import YouTube

from services.assistant.assistant_pb2 import MessageResponse
from services.assistant.assistant_pb2 import SendVideoRequest
from services.assistant.grpc.client import AssistantGrpcClient
from utils.common.patterns import Factory
from utils.post.exceptions import PostNonDownloadable
from utils.post.exceptions import PostTooLarge
from utils.post.exceptions import PostUnavailable
from utils.telegram.protocols import SupportsTelegramSending


class Post(ABC, SupportsTelegramSending):
    @property
    @abstractmethod
    def id(self) -> str:
        """
        :return: Post ID
        """
        pass

    @abstractmethod
    def download(self, out_dir: str) -> os.PathLike:
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
    def init_from_id(id_: str) -> "Post":
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
        class_name, id_ = post_id.split(":")
        subclasses = {class_.__name__: class_ for class_ in Post.__subclasses__()}
        return subclasses[class_name].init_from_id(id_)


class YouTubeShortVideo(Post):
    YT_SHORT_VIDEO_TTL = timedelta(minutes=3)
    YT_SHORT_VIDEO_MAX_LEN = timedelta(minutes=3)

    def __init__(self, url: str):
        self.url = url

        try:
            self.yt = YouTube(self.url)
        except pytube.exceptions.VideoUnavailable:
            raise PostUnavailable(self.url)

        video_len = timedelta(seconds=self.yt.length)
        if video_len > self.YT_SHORT_VIDEO_MAX_LEN:
            raise PostTooLarge(url)

    @property
    def id(self) -> str:
        return f"{type(self).__name__}:{self.yt.video_id}"

    def download(self, out_dir: str) -> os.PathLike:
        """
        Download short YouTube video.

        :param out_dir: Output directory
        :return: Output filename
        """
        stream = self.yt.streams.get_highest_resolution()
        if stream is None:
            raise PostNonDownloadable(self.url)
        uniq_filename = f"{self.id}.{stream.subtype}"
        out_filename = stream.download(out_dir, uniq_filename)
        return out_filename

    def clear(self, out_filename: str) -> None:
        if path.exists(out_filename):
            os.remove(out_filename)

    @property
    def ttl(self) -> timedelta:
        return self.YT_SHORT_VIDEO_TTL

    @property
    def title(self) -> str:
        return self.yt.title

    def send(self, client: AssistantGrpcClient, **kwargs) -> MessageResponse:
        req = SendVideoRequest(caption=self.title, **kwargs)
        return client.stub.send_video(req)

    @staticmethod
    def init_from_id(id_: str) -> "YouTubeShortVideo":
        url = f"https://www.youtube.com/watch?v={id_}"
        return YouTubeShortVideo(url)


# class TikTokVideo(Post):
#     TT_VIDEO_TTL = timedelta(minutes=3)
#     TT_VIDEO_MAX_LEN = timedelta(minutes=3)
#
#     def __init__(self, url: str):
#         self.url = url
#
#         # TODO: check for available video
#         # TODO: add check for video size
#         self.tiktok_api = TikTokApi()
#         self.video = self.tiktok_api.video(url=self.url)
#
#     @property
#     def id(self) -> str:
#         return f'{type(self).__name__}:{self.video.id}'
#
#     def download(self, out_dir: str) -> str:
#         with self.tiktok_api:
#             video_data = self.video.bytes()
#             video_path = os.path.join(out_dir, self.id)
#             with open(video_path, "wb") as out_file:
#                 out_file.write(video_data)
#
#         return video_path
#
#     @property
#     def ttl(self) -> timedelta:
#         return self.TT_VIDEO_TTL
#
#     @property
#     def title(self) -> str:
#         # TODO: handle if something wrong
#         info = self.video.info()
#         return info['desc']
#
#     def clear(self, out_filename: str) -> None:
#         if os.path.exists(out_filename):
#             os.remove(out_filename)
#
#     @staticmethod
#     def init_from_id(id_: str) -> 'Post':
#         url = f'https://www.tiktok.com/embed/video/{id_}'
#         return TikTokVideo(url)
