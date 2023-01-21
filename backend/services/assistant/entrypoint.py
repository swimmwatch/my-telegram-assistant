"""
Assistant entrypoint.
"""
from grpc import aio
from loguru import logger

from services.assistant import assistant_pb2_grpc
from services.assistant.assistant import Assistant
from services.assistant.config import assistant_settings
from services.assistant.grpc.server import AsyncAssistantService


class AssistantEntrypoint:
    def __init__(self, assistant: Assistant):
        self.assistant = assistant

    async def run_grpc_server(self):
        """
        Run gRPC server.
        """
        server = aio.server()
        assistant_pb2_grpc.add_AssistantServicer_to_server(
            AsyncAssistantService(self.assistant), server
        )
        server.add_insecure_port(assistant_settings.assistant_grpc_addr)

        logger.info(f"starting gRPC server on {assistant_settings.assistant_grpc_addr}")
        await server.start()
        await self.assistant.init()  # connect to Telegram inside gRPC process
        await server.wait_for_termination()

    async def run(self):
        await self.run_grpc_server()
