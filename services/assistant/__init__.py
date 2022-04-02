"""
Assistant service package.
"""
import aiotdlib
from google.protobuf.empty_pb2 import Empty

from services.assistant.assistant_pb2 import MessageResponse
from services.assistant.assistant_pb2_grpc import AssistantServicer


class AsyncAssistantService(AssistantServicer):
    def __init__(self, aiotdlib_client: aiotdlib.Client):
        super().__init__()

        self.aiotdlib_client = aiotdlib_client

    async def send_text(self, request, context) -> Empty:
        # TODO: handle errors from Aiotdlib
        result_msg = await self.aiotdlib_client.send_text(
            request.chat_id,
            request.text,
            disable_notification=request.disable_notification
        )
        return MessageResponse(
            id=result_msg,
            chat_id=result_msg.chat_id,
            can_be_forwarded=result_msg.can_be_forwarded
        )

    async def send_video(self, request, context):
        # TODO: handle errors from Aiotdlib
        result_msg = await self.aiotdlib_client.send_video(
            request.chat_id,
            request.video_path,
            caption=request.caption,
            disable_notification=request.disable_notification
        )
        return MessageResponse(
            id=result_msg.id,
            chat_id=result_msg.chat_id,
            can_be_forwarded=result_msg.can_be_forwarded
        )

    async def forward_messages(self, request, context):
        # TODO: handle errors from Aiotdlib
        await self.aiotdlib_client.forward_messages(
            request.from_chat_id,
            request.chat_id,
            list(request.message_ids),
            disable_notification=request.disable_notification
        )
        return Empty()
