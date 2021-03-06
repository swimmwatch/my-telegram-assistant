import asyncio
import logging

import aiotdlib
from aiotdlib import Client
from aiotdlib.api import API, UpdateNewMessage
from grpc import aio
from loguru import logger

from app.container import Container
from services.assistant import assistant_pb2_grpc, AsyncAssistantService
from services.assistant.commands import CommandRequest, ExplicitCommandHandlerWrapper
from services.assistant.config import AIOTDLIB_API_ID, AIOTDLIB_API_HASH, PHONE_NUMBER, ASSISTANT_GRPC_ADDR
from services.assistant.handlers.about_me import about_me_command
from services.assistant.handlers.all import all_command
from services.assistant.handlers.download_post import YouTubeShortVideoDownloadCommandHandler, \
    reply_download_post_command
from services.assistant.handlers.hello import hello_command
from utils.aiotdlib.client import CustomClient
from utils.aiotdlib.decorators import serve_only_own_actions


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


async def run_grpc_server(aiotdlib_client: aiotdlib.Client):
    server = aio.server()
    assistant_pb2_grpc.add_AssistantServicer_to_server(AsyncAssistantService(aiotdlib_client), server)
    server.add_insecure_port(ASSISTANT_GRPC_ADDR)

    logger.info(f'starting gRPC server on {ASSISTANT_GRPC_ADDR}')
    await server.start()
    await server.wait_for_termination()


async def run_assistant(aiotdlib_client: aiotdlib.Client):
    async with aiotdlib_client:
        await aiotdlib_client.idle()


@serve_only_own_actions
async def handle_new_own_message(client: Client, update: UpdateNewMessage):
    command_request = CommandRequest(
        client=client,
        message=update.message
    )
    await CommandsManager.handle(command_request)


async def main():
    aiotdlib_client = CustomClient(
        api_id=AIOTDLIB_API_ID,
        api_hash=AIOTDLIB_API_HASH,
        phone_number=PHONE_NUMBER,
    )
    aiotdlib_client.add_event_handler(handle_new_own_message, update_type=API.Types.UPDATE_NEW_MESSAGE)

    await asyncio.gather(
        run_assistant(aiotdlib_client),
        run_grpc_server(aiotdlib_client)
    )


if __name__ == '__main__':
    container = Container()
    container.wire(modules=[__name__])

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
