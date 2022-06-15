"""
Download post command handler.
"""
from loguru import logger

from services.assistant.commands import CommandRequest, ParsedArguments, ExplicitCommand
from services.assistant.commands.decorators import serve_only_replied_request
from utils.common.patterns import AsyncChainOfResponsibility
from utils.post.impl import YouTubeShortVideo
from utils.youtube import extract_youtube_link
from services.worker.app import download_and_send_post


class YouTubeShortVideoDownloadCommandHandler(AsyncChainOfResponsibility):
    async def process_request(self, request: CommandRequest) -> bool:
        if request.text is None:
            return False

        link = extract_youtube_link(request.text)
        if not link:
            return False

        # remove web page preview
        if not request.replied:
            await request.client.edit_text(
                request.message.chat_id,
                request.message.id,
                text=request.text,
                disable_web_page_preview=True
            )

        post = YouTubeShortVideo(link)
        download_and_send_post.delay(request.message.chat_id, post.id)
        logger.info(f'downloading YouTube short video post: {link}')

        return True


reply_download_post_command = ExplicitCommand(name="d")


@reply_download_post_command.on()
@serve_only_replied_request
async def handle_replied_download_post_call(_: ParsedArguments, request: CommandRequest):
    replied_message = await request.client.api.get_message(
        request.message.chat_id,
        request.message.reply_to_message_id
    )
    inner_req = CommandRequest(
        message=replied_message,
        client=request.client,
        replied=True
    )
    yt_handler = YouTubeShortVideoDownloadCommandHandler(None)
    await yt_handler.process_request(inner_req)
