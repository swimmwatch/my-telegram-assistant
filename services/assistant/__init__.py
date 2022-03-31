"""
Assistant service package.
"""
import aiotdlib
from google.protobuf.empty_pb2 import Empty

from services.assistant.assistant_pb2_grpc import AssistantServicer


class AsyncAssistantService(AssistantServicer):
    def __init__(self, aiotdlib_client: aiotdlib.Client):
        super().__init__()

        self.aiotdlib_client = aiotdlib_client

    async def send_text(self, request, context) -> Empty:
        # TODO: handle errors from Aiotdlib
        await self.aiotdlib_client.send_text(
            request.chat_id,
            request.text,
            disable_notification=request.disable_notification
        )
        return Empty()

    async def send_video(self, request, context):
        raise NotImplementedError
