import asyncio
import logging

import qrcode
from dependency_injector.wiring import inject, Provide
from grpc import aio
from loguru import logger
from telethon import TelegramClient, events

from services.assistant import assistant_pb2_grpc
from services.assistant.container import AssistantContainer
from services.assistant.grpc.server import AsyncAssistantService
from services.assistant.commands import CommandRequest, ExplicitCommandHandlerWrapper
from services.assistant.config import assistant_settings
from services.assistant.handlers.about_me import about_me_command
from services.assistant.handlers.all import all_command
from services.assistant.handlers.download_post import YouTubeShortVideoDownloadCommandHandler, \
    reply_download_post_command
from services.assistant.handlers.hello import hello_command
from services.assistant_manager.assistant_manager_pb2 import SendPhotoRequest, SendTextRequest
from services.assistant_manager.config import assistant_manager_settings
from services.assistant_manager.grpc.client import AssistantManagerGrpcClient
from utils.img.base64 import Base64Image


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


async def run_grpc_server(telegram_client: TelegramClient):
    server = aio.server()
    assistant_pb2_grpc.add_AssistantServicer_to_server(AsyncAssistantService(telegram_client), server)
    server.add_insecure_port(assistant_settings.assistant_grpc_addr)

    logger.info(f'starting gRPC server on {assistant_settings.assistant_grpc_addr}')
    await server.start()
    await server.wait_for_termination()


@inject
async def run_assistant(
        telegram_client: TelegramClient,
        assistant_manager_grpc_client: AssistantManagerGrpcClient =
        Provide[AssistantContainer.assistant_manager_grpc_client]
):
    # TODO: refactor authorize
    await telegram_client.connect()
    is_user_authorized = await telegram_client.is_user_authorized()
    if not is_user_authorized:
        qr_login = await telegram_client.qr_login()
        img = qrcode.make(qr_login.url)
        base64_img = Base64Image.encode(img)
        req = SendPhotoRequest(
            chat_id=assistant_manager_settings.my_telegram_id,
            caption='Please login using this QR code.',
            base64_img=base64_img
        )
        assistant_manager_grpc_client.stub.send_photo(req)
        user = await qr_login.wait(assistant_settings.assistant_qr_login_timeout)
        if user:
            req = SendTextRequest(
                chat_id=assistant_manager_settings.my_telegram_id,
                text='You were authorized successful!'
            )
            assistant_manager_grpc_client.stub.send_text(req)


async def main():
    telegram_client = TelegramClient(
        'anon',
        assistant_settings.aiotdlib_api_id,
        assistant_settings.aiotdlib_api_hash,
    )

    @telegram_client.on(events.NewMessage(outgoing=True))
    async def handle_new_own_message(event: events.NewMessage.Event):
        command_request = CommandRequest(event)
        await CommandsManager.handle(command_request)

    await asyncio.gather(
        run_assistant(telegram_client),
        run_grpc_server(telegram_client)
    )


if __name__ == '__main__':
    assistant_container = AssistantContainer()
    assistant_container.wire(modules=[__name__])

    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
