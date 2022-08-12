"""
Assistant entrypoint.
"""
import asyncio

from grpc import aio
from loguru import logger

from services.assistant import assistant_pb2_grpc
from services.assistant.assistant import Assistant
from services.assistant.config import assistant_settings
from services.assistant.grpc.server import AsyncAssistantService


class AssistantEntrypoint:
    def __init__(
            self,
            assistant: Assistant
    ):
        self.assistant = assistant

    async def run_grpc_server(self):
        """
        Run gRPC server.
        """
        server = aio.server()
        assistant_pb2_grpc.add_AssistantServicer_to_server(
            AsyncAssistantService(self.assistant.telegram_client),
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
        is_user_authorized = await self.assistant.is_user_authorized()
        if not is_user_authorized:
            await self.assistant.authorize_user()

    async def run(self):
        """
        Run assistant service.
        """
        await self.assistant.init()

        await asyncio.gather(
            self.run_assistant(),
            self.run_grpc_server()
        )
