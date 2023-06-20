"""
Download post command handler.
"""
from loguru import logger
from telethon import events
from telethon.errors import MessageNotModifiedError

from services.assistant.commands import CommandRequest, ExplicitCommand, ParsedArguments
from services.assistant.commands.decorators import serve_only_replied_request
from services.assistant.tasks import download_and_send_post
from utils.common.patterns import AsyncChainOfResponsibility
from utils.post.exceptions import PostTooLarge, PostUnavailable
from utils.post.impl import YouTubeShortVideo
from utils.youtube import extract_youtube_link


class YouTubeShortVideoDownloadCommandHandler(AsyncChainOfResponsibility):
    async def process_request(self, request: CommandRequest) -> bool:
        if request.text is None:
            return False

        link = extract_youtube_link(request.text)
        if not link:
            return False

        try:
            _ = YouTubeShortVideo(link)
        except (PostTooLarge, PostUnavailable):
            return False

        # remove web page preview
        if not request.event.message.is_reply:
            try:
                # space for avoid MessageNotModifiedError
                await request.event.message.edit(request.text + " ", link_preview=False)
            except MessageNotModifiedError:
                logger.warning("link preview was not hidden.")

        post = YouTubeShortVideo(link)
        download_and_send_post.delay(request.event.message.chat_id, post.id)
        logger.info(f"downloading YouTube short video post: {link}")

        return True


reply_download_post_command = ExplicitCommand(name="d")


@reply_download_post_command.on()
@serve_only_replied_request
async def handle_replied_download_post_call(_: ParsedArguments, request: CommandRequest):
    replied_message = await request.event.message.get_reply_message()
    inner_req = CommandRequest(events.NewMessage.Event(replied_message))
    yt_handler = YouTubeShortVideoDownloadCommandHandler(None)
    await yt_handler.process_request(inner_req)
