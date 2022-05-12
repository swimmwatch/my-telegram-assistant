from aiotdlib import Client
from loguru import logger

from services.assistant.commands import CommandRequest, ExplicitCommand, ParsedArguments
from services.worker.app import download_and_send_post
from utils.common.patterns import AsyncChainOfResponsibility
from utils.post.impl import YouTubeShortVideo
from utils.youtube import extract_youtube_link


class YouTubeShortVideoDownloadCommandHandler(AsyncChainOfResponsibility):
    async def process_request(self, request: CommandRequest) -> bool:
        link = extract_youtube_link(request.message)
        if not link:
            return False

        post = YouTubeShortVideo(link)
        download_and_send_post.delay(request.chat_id, post.id)
        logger.info(f'downloading YouTube short video post: {link}')

        return True


about_me_command = ExplicitCommand(name="me").add_arg(name='type', type_=str)


@about_me_command.on
async def handle_output_work_profile(args: ParsedArguments, client: Client, command_request: CommandRequest):
    if args['type'] == 'work':
        await client.send_text(command_request.chat_id, 'I am working!')


@about_me_command.on
async def handle_output_game_profile(args: ParsedArguments, client: Client, command_request: CommandRequest):
    if args['type'] == 'game':
        await client.send_text(command_request.chat_id, 'I am gaming!')


class AboutMeCommandHandler(AsyncChainOfResponsibility):
    async def process_request(self, request: CommandRequest) -> bool:
        args = about_me_command.parse(request.message)
        if not args:
            return False

        await about_me_command.emit(args, request.client, request)
        logger.info('handling about me command')

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
