from typing import NamedTuple

from loguru import logger

from utils.common.patterns import ChainOfResponsibility
# from utils.post.impl import TikTokVideo
from utils.post.impl import YouTubeShortVideo
# from utils.tiktok import extract_tiktok_link
from utils.youtube import extract_youtube_link
from services.worker.app import download_and_send_post


class CommandRequest(NamedTuple):
    message: str
    chat_id: int


class YouTubeShortVideoDownloadCommandHandler(ChainOfResponsibility):
    def process_request(self, request: CommandRequest) -> bool:
        link = extract_youtube_link(request.message)
        if not link:
            return False

        post = YouTubeShortVideo(link)
        download_and_send_post.delay(request.chat_id, post.id)
        logger.info(f'downloading YouTube short video post: {link}')

        return True


# class TikTokVideoDownloadCommandHandler(ChainOfResponsibility):
#     def process_request(self, request: CommandRequest) -> bool:
#         link = extract_tiktok_link(request.message)
#         if not link:
#             return False
#
#         post = TikTokVideo(link)
#         download_and_send_post.delay(request.chat_id, post.id)
#         logger.info(f'downloading TikTok post: {link}')
#
#         return True
