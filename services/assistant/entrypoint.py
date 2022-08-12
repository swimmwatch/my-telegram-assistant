"""
Assistant entrypoint.
"""
import asyncio

import qrcode
from grpc import aio
from loguru import logger
from telethon import TelegramClient

from services.assistant import assistant_pb2_grpc
from services.assistant.config import assistant_settings
from services.assistant.grpc.server import AsyncAssistantService
from services.assistant_manager.assistant_manager_pb2 import SendTextRequest, SendPhotoRequest
from services.assistant_manager.config import assistant_manager_settings
from services.assistant_manager.grpc.client import AssistantManagerGrpcClient
from utils.img.base64 import Base64Image


class AssistantEntrypoint:
    def __init__(
            self,
            telegram_client: TelegramClient,
            assistant_manager_grpc_client: AssistantManagerGrpcClient
    ):
        self.telegram_client = telegram_client
        self.assistant_manager_grpc_client = assistant_manager_grpc_client

    async def run_grpc_server(self):
        """
        Run gRPC server.
        """
        server = aio.server()
        assistant_pb2_grpc.add_AssistantServicer_to_server(
            AsyncAssistantService(self.telegram_client),
            server
        )
        server.add_insecure_port(assistant_settings.assistant_grpc_addr)

        logger.info(f'starting gRPC server on {assistant_settings.assistant_grpc_addr}')
        await server.start()
        await server.wait_for_termination()

    async def run_assistant(self):
        """
        Run Telegram client.
        """
        # TODO: refactor authorize
        await self.telegram_client.connect()
        is_user_authorized = await self.telegram_client.is_user_authorized()
        if not is_user_authorized:
            qr_login = await self.telegram_client.qr_login()
            img = qrcode.make(qr_login.url)
            base64_img = Base64Image.encode(img)
            req = SendPhotoRequest(
                chat_id=assistant_manager_settings.my_telegram_id,
                caption='Please login using this QR code.',
                base64_img=base64_img
            )
            self.assistant_manager_grpc_client.stub.send_photo(req)
            user = await qr_login.wait(assistant_settings.assistant_qr_login_timeout)
            req = SendTextRequest(
                chat_id=assistant_manager_settings.my_telegram_id,
                text=f'{user.username}, authorized successful!'
            )
            self.assistant_manager_grpc_client.stub.send_text(req)

    async def run(self):
        """
        Run assistant service.
        """
        await asyncio.gather(
            self.run_assistant(),
            self.run_grpc_server()
        )
