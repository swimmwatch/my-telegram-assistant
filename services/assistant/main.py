import asyncio
import logging

from telethon import events

from services.assistant.container import AssistantContainer
from services.assistant.commands import CommandRequest, ExplicitCommandHandlerWrapper
from services.assistant.handlers.about_me import about_me_command
from services.assistant.handlers.all import all_command
from services.assistant.handlers.download_post import YouTubeShortVideoDownloadCommandHandler, \
    reply_download_post_command
from services.assistant.handlers.hello import hello_command


class CommandsManager:
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


async def main():
    assistant_container = AssistantContainer()
    assistant_container.wire(modules=[__name__])

    telegram_client = assistant_container.telegram_client()
    assistant_entrypoint = assistant_container.assistant_entrypoint()

    @telegram_client.on(events.NewMessage(outgoing=True))
    async def handle_new_own_message(event: events.NewMessage.Event):
        command_request = CommandRequest(event)
        await CommandsManager.handle(command_request)

    await assistant_entrypoint.run()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
