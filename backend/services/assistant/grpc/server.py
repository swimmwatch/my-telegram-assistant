"""
gRPC Assistant server.
"""
from google.protobuf.empty_pb2 import Empty
from grpc import StatusCode

from services.assistant.assistant import Assistant
from services.assistant.assistant_pb2 import BooleanValue, MessageResponse
from services.assistant.assistant_pb2_grpc import AssistantServicer


class AsyncAssistantService(AssistantServicer):
    def __init__(self, assistant: Assistant):
        super().__init__()

        self.assistant = assistant
        self.telegram_client = self.assistant.telegram_client

    async def send_text(self, request, context) -> Empty:
        # TODO: handle errors
        result_msg = await self.telegram_client.send_message(
            request.chat_id, message=request.text, silent=request.disable_notification
        )
        return MessageResponse(
            id=result_msg.id,
            chat_id=request.chat_id,
            # can_be_forwarded=result_msg.can_be_forwarded
        )

    async def send_video(self, request, context):
        # TODO: handle errors
        result_msg = await self.telegram_client.send_file(
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

    async def forward_messages(self, request, context):
        # TODO: handle errors
        await self.telegram_client.forward_messages(
            request.from_chat_id,
            list(request.message_ids),
            request.chat_id,
            silent=request.disable_notification,
        )
        return Empty()

    async def is_user_authorized(self, request, context):
        is_user_authorized = await self.assistant.is_user_authorized()
        return BooleanValue(value=is_user_authorized)

    async def authorize_user(self, request, context):
        is_connected = self.telegram_client.is_connected()
        if not is_connected:
            await self.telegram_client.connect()

        is_user_authorized = await self.assistant.is_user_authorized()
        if not is_user_authorized:
            # TODO: Handle too much attempts error.
            await self.assistant.authorize_user()
        else:
            detail_msg = "You are already logged in."
            context.set_code(StatusCode.ALREADY_EXISTS)
            context.set_details(detail_msg)

        return Empty()

    async def logout_user(self, request, context):
        is_user_authorized = await self.assistant.is_user_authorized()
        if is_user_authorized:
            status = await self.telegram_client.log_out()

            if not status:
                detail_msg = "Something wrong with logout."
                context.set_code(StatusCode.CANCELLED)
                context.set_details(detail_msg)
        else:
            detail_msg = "You are not authorized."
            context.set_code(StatusCode.UNAUTHENTICATED)
            context.set_details(detail_msg)

        return Empty()
