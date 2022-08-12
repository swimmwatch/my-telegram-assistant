"""
Assistant.
"""
from telethon import TelegramClient, events

from services.assistant.commands import CommandRequest, ExplicitCommandHandlerWrapper
from services.assistant.handlers.about_me import about_me_command
from services.assistant.handlers.all import all_command
from services.assistant.handlers.download_post import YouTubeShortVideoDownloadCommandHandler, \
    reply_download_post_command
from services.assistant.handlers.hello import hello_command


class AssistantCommandsManager:
    """
    Commands manager.
    """
    _commands = YouTubeShortVideoDownloadCommandHandler(
        ExplicitCommandHandlerWrapper(
            about_me_command,
            ExplicitCommandHandlerWrapper(
                hello_command,
                ExplicitCommandHandlerWrapper(
                    reply_download_post_command,
                    ExplicitCommandHandlerWrapper(
                        all_command
                    )
                )
            )
        )
    )

    @classmethod
    async def handle(cls, request: CommandRequest):
        await cls._commands.handle(request)


class Assistant:
    def __init__(self, telegram_client: TelegramClient):
        self.telegram_client = telegram_client

    def _add_handlers(self):
        """
        Add Telegram handlers.
        """
        @self.telegram_client.on(events.NewMessage(outgoing=True))
        async def handle_new_own_message(event: events.NewMessage.Event):
            command_request = CommandRequest(event)
            await AssistantCommandsManager.handle(command_request)

    def init(self):
        """
        Assistant initialization.
        """
        self._add_handlers()
