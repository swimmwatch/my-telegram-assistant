"""
gRPC Assistant server.
"""
import asyncio

import qrcode
from google.protobuf.empty_pb2 import Empty
from grpc import StatusCode
from PIL.Image import Image
from telethon.errors import SessionPasswordNeededError
from telethon.sessions import StringSession
from telethon.tl.custom import QRLogin
from telethon.tl.types import User as TelethonUser

from services.assistant.assistant_pb2 import AuthMethod
from services.assistant.assistant_pb2 import BooleanValue
from services.assistant.assistant_pb2 import MessageResponse
from services.assistant.assistant_pb2_grpc import AssistantServicer
from services.assistant.client import AssistantClient
from services.assistant.config import AssistantSettings
from services.bot.bot_pb2 import SendPhotoRequest
from services.bot.bot_pb2 import SendTextRequest
from services.bot.grpc_.client import TelegramBotAsyncGrpcClient
from services.db.dal import UserAsyncDAL
from utils.img.base64 import Base64Image
from utils.sqlalchemy.types import AsyncSessionFactory


class AsyncAssistantService(AssistantServicer):
    def __init__(
        self,
        assistant: AssistantClient,
        bot_grpc_client: TelegramBotAsyncGrpcClient,
        session_factory: AsyncSessionFactory,
    ) -> None:
        super().__init__()

        self.assistant = assistant
        self.bot_grpc_client = bot_grpc_client

        self.session_factory = session_factory
        self.user_repo = UserAsyncDAL(self.session_factory)

        self.assistant_settings = AssistantSettings()

    async def send_text(self, request, context):
        # TODO: handle errors
        result_msg = await self.assistant.telegram_client.send_message(
            request.chat_id,
            message=request.text,
            silent=request.disable_notification,
        )
        return MessageResponse(
            id=result_msg.id,
            chat_id=request.chat_id,
            # can_be_forwarded=result_msg.can_be_forwarded
        )

    async def send_video(self, request, context):
        # TODO: handle errors
        result_msg = await self.assistant.telegram_client.send_file(
            request.chat_id,
            request.video_path,
            caption=request.caption,
            silent=request.disable_notification,
        )
        return MessageResponse(
            id=result_msg.id,
            chat_id=request.chat_id,
            # can_be_forwarded=result_msg.can_be_forwarded
        )

    async def send_files(self, request, context):
        # TODO: handle errors
        messages = await self.assistant.telegram_client.send_file(
            request.chat_id,
            list(request.files),
            caption=request.caption,
            silent=request.disable_notification,
        )
        return MessageResponse(
            id=messages[0].id,
            chat_id=request.chat_id,
            # can_be_forwarded=result_msg.can_be_forwarded
        )

    async def forward_messages(self, request, context):
        # TODO: handle errors
        await self.assistant.telegram_client.forward_messages(
            request.chat_id,
            list(request.message_ids),
            request.from_chat_id,
            silent=request.disable_notification,
        )
        return Empty()

    async def is_authorized(self, request, context):
        is_authorized = await self.assistant.is_authorized()
        return BooleanValue(value=is_authorized)

    def _create_login_qr_code(self, qr_login: QRLogin) -> Image:
        return qrcode.make(qr_login.url)

    async def _send_qr_code(self, chat_id: int, img: Image) -> None:
        base64_img = Base64Image.encode(img)
        req = SendPhotoRequest(
            chat_id=chat_id,
            caption="Please login using this QR code.",
            base64_img=base64_img,
        )
        await self.bot_grpc_client.stub.send_photo(req)

    async def _authorize_qr_login(self, tg_user_id: int, two_fa_password: str) -> TelethonUser:
        qr_login = await self.assistant.telegram_client.qr_login()
        user: TelethonUser | None = None
        attempts = 1
        while not user:
            if attempts > 3:
                break

            img = self._create_login_qr_code(qr_login)
            await self._send_qr_code(tg_user_id, img)
            try:
                user = await qr_login.wait(self.assistant_settings.qr_login_timeout)
            except SessionPasswordNeededError as err:
                if not two_fa_password:
                    raise err
                user = await self._authorize_2fa_password(two_fa_password)
            except asyncio.TimeoutError:
                await qr_login.recreate()
                attempts += 1
        return user

    async def _authorize_2fa_password(self, password: str) -> TelethonUser:
        return await self.assistant.telegram_client.sign_in(password=password)

    async def _authorize_user(
        self,
        tg_user_id: int,
        auth_method: AuthMethod,
        two_fa_password: str | None = None,
    ) -> TelethonUser:
        current_user = self.user_repo.filter(tg_id=tg_user_id)
        user = await current_user.first()

        # TODO: Handle session decryption/encryption
        session = StringSession(user.session)
        self.assistant.client_factory(session)
        await self.assistant.connect()

        is_authorized = await self.assistant.is_authorized()
        if not is_authorized:
            match auth_method:
                case AuthMethod.QR_CODE:
                    user = await self._authorize_qr_login(tg_user_id, two_fa_password)
                case AuthMethod.PHONE:
                    pass
                case _:
                    pass
        else:
            user = await self.assistant.get_me()

        # Save new Telegram session for current user
        if user:
            session = self.assistant.get_session()
            await current_user.update(session=session)

        return user

    async def _send_success_msg(self, chat_id: int, username: str):
        req = SendTextRequest(
            chat_id=chat_id,
            text=f"{username}, authorized successful!",
        )
        await self.bot_grpc_client.stub.send_text(req)

    async def authorize_user(self, request, context):
        telegram_user: TelethonUser | None = None
        is_authorized = await self.assistant.is_authorized()
        if not is_authorized:
            try:
                # TODO: handle unknown authorization method
                telegram_user = await self._authorize_user(
                    request.tg_user_id,
                    request.auth_method,
                    request.two_fa_password,
                )
            except SessionPasswordNeededError:
                # Handle case if you need to pass two factor password
                detail_msg = "Cannot authorize. Need pass two factory password."
                context.set_details(detail_msg)
                context.set_code(StatusCode.CANCELLED)

            if not telegram_user:
                detail_msg = "Cannot authorize. Try later."
                context.set_code(StatusCode.CANCELLED)
                context.set_details(detail_msg)
            else:
                await self.assistant.init()
                await self._send_success_msg(request.tg_user_id, telegram_user.username)
        else:
            detail_msg = "You are already logged in."
            context.set_code(StatusCode.ALREADY_EXISTS)
            context.set_details(detail_msg)

        return Empty()

    async def logout_user(self, request, context):
        is_authorized = await self.assistant.is_authorized()
        if is_authorized:
            status = await self.assistant.log_out()

            if not status:
                detail_msg = "Something wrong with logout."
                context.set_code(StatusCode.CANCELLED)
                context.set_details(detail_msg)
        else:
            detail_msg = "You are not authorized."
            context.set_code(StatusCode.UNAUTHENTICATED)
            context.set_details(detail_msg)

        return Empty()
