"""
Assistant.
"""
import asyncio

import qrcode
from PIL.Image import Image
from telethon import TelegramClient
from telethon import events
from telethon.errors import SessionPasswordNeededError
from telethon.tl.custom import QRLogin

from services.assistant.commands import CommandRequest
from services.assistant.commands import ExplicitCommandHandlerWrapper
from services.assistant.config import AssistantSettings
from services.assistant.handlers.about_me import about_me_command
from services.assistant.handlers.all import all_command
from services.assistant.handlers.download_post import (
    InstagramPostDownloadCommandHandler,
)
from services.assistant.handlers.download_post import (
    YouTubeShortVideoDownloadCommandHandler,
)
from services.assistant.handlers.download_post import reply_download_post_command
from services.assistant.handlers.hello import hello_command
from services.assistant_manager.assistant_manager_pb2 import SendPhotoRequest
from services.assistant_manager.assistant_manager_pb2 import SendTextRequest
from services.assistant_manager.config import AssistantManagerSettings
from services.assistant_manager.grpc_.client import AssistantManagerGrpcClient
from utils.img.base64 import Base64Image


class AssistantCommandsManager:
    """
    Commands manager.
    """

    _commands = YouTubeShortVideoDownloadCommandHandler(
        InstagramPostDownloadCommandHandler(
            ExplicitCommandHandlerWrapper(
                about_me_command,
                ExplicitCommandHandlerWrapper(
                    hello_command,
                    ExplicitCommandHandlerWrapper(
                        reply_download_post_command,
                        ExplicitCommandHandlerWrapper(all_command),
                    ),
                ),
            )
        )
    )

    @classmethod
    async def handle(cls, request: CommandRequest):
        await cls._commands.handle(request)


class Assistant:
    def __init__(
        self,
        telegram_client: TelegramClient,
        assistant_manager_grpc_client: AssistantManagerGrpcClient,
    ):
        self.settings = AssistantSettings()  # type: ignore
        self.assistant_manager_settings = AssistantManagerSettings()  # type: ignore
        self.telegram_client = telegram_client
        self.assistant_manager_grpc_client = assistant_manager_grpc_client

    def _add_handlers(self):
        """
        Add Telegram handlers.
        """

        @self.telegram_client.on(events.NewMessage(outgoing=True))
        async def handle_new_own_message(event: events.NewMessage.Event):
            command_request = CommandRequest(event)
            await AssistantCommandsManager.handle(command_request)

    async def is_user_authorized(self) -> bool:
        return await self.telegram_client.is_user_authorized()

    def _create_login_qr_code(self, qr_login: QRLogin) -> Image:
        return qrcode.make(qr_login.url)

    def _send_qr_code(self, img: Image):
        base64_img = Base64Image.encode(img)
        req = SendPhotoRequest(
            chat_id=self.assistant_manager_settings.my_telegram_id,
            caption="Please login using this QR code.",
            base64_img=base64_img,
        )
        self.assistant_manager_grpc_client.stub.send_photo(req)

    async def authorize_user(self):
        qr_login = await self.telegram_client.qr_login()
        user = None
        while not user:
            # TODO: Add attempts counting process. If too much the raise exception.
            img = self._create_login_qr_code(qr_login)
            self._send_qr_code(img)
            try:
                user = await qr_login.wait(self.settings.qr_login_timeout)
            except asyncio.TimeoutError:
                await qr_login.recreate()

        req = SendTextRequest(
            chat_id=self.assistant_manager_settings.my_telegram_id,
            text=f"{user.username}, authorized successful!",
        )
        self.assistant_manager_grpc_client.stub.send_text(req)

    async def init(self):
        """
        Assistant initialization.
        """
        self._add_handlers()
        await self.telegram_client.connect()
