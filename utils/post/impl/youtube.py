"""
YouTube post implementation.
"""
import os.path
from datetime import timedelta
from os import path
from pathlib import Path

import pytube.exceptions
from pytube import YouTube

from services.assistant.assistant_pb2 import SendVideoRequest, MessageResponse
from services.assistant.grpc_client import AssistantGrpcClient
from utils.post.impl import Post
from utils.post.exceptions import PostUnavailable, PostNonDownloadable, PostTooLarge


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
        return f'{type(self).__name__}:{self.yt.video_id}'

    def download(self, out_dir: str) -> str:
        """
        Download short YouTube video.

        :param out_dir: Output directory
        :return: Output filename
        """
        stream = self.yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
        if stream is None:
            raise PostNonDownloadable(self.url)
        out_filename = stream.download(out_dir, self.id)
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
    def init_from_id(id_: str) -> 'YouTubeShortVideo':
        url = f'https://www.youtube.com/watch?v={id_}'
        return YouTubeShortVideo(url)
