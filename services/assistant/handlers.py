from aiotdlib import Client
from aiotdlib.api import UpdateNewMessage, MessageText

from services.assistant.commands import YouTubeShortVideoDownloadCommandHandler, CommandRequest
from utils.aiotdlib.decorators import serve_only_own_actions


commands = YouTubeShortVideoDownloadCommandHandler(None)


@serve_only_own_actions
async def handle_new_own_message(client: Client, update: UpdateNewMessage):
    chat_id = update.message.chat_id

    content = update.message.content
    if not isinstance(content, MessageText):
        return

    formatted_text = content.text
    msg = formatted_text.text

    # remove web page preview
    await client.edit_text(
        chat_id,
        update.message.id,
        text=msg,
        disable_web_page_preview=True
    )

    command_request = CommandRequest(message=msg, chat_id=chat_id)
    commands.handle(command_request)
