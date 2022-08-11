"""
gRPC Assistant server.
"""
from google.protobuf.empty_pb2 import Empty
from telethon import TelegramClient

from services.assistant.assistant_pb2 import MessageResponse
from services.assistant.assistant_pb2_grpc import AssistantServicer


class AsyncAssistantService(AssistantServicer):
    def __init__(self, telegram_client: TelegramClient):
        super().__init__()

        self.telegram_client = telegram_client

    async def send_text(self, request, context) -> Empty:
        # TODO: handle errors
        result_msg = await self.telegram_client.send_message(
            request.chat_id,
            message=request.text,
            silent=request.disable_notification
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
            silent=request.disable_notification
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
            silent=request.disable_notification
        )
        return Empty()
