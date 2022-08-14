"""
Assistant manager entrypoint service.
"""
import asyncio
from multiprocessing import Process

from aiogram import Dispatcher
from grpc import aio
from loguru import logger

from services.assistant_manager import assistant_manager_pb2_grpc
from services.assistant_manager.bot import bot
from services.assistant_manager.config import assistant_manager_settings
from services.assistant_manager.grpc.server import AsyncAssistantManagerService


class AssistantManagerEntrypoint:
    def __init__(self, dp: Dispatcher):
        self.dp = dp

    async def run_bot(self):
        logger.info('launch bot')
        await self.dp.start_polling()

    async def run_grpc_server(self):
        server = aio.server()
        assistant_manager_pb2_grpc.add_AssistantManagerServicer_to_server(
            AsyncAssistantManagerService(bot),
            server
        )
        server.add_insecure_port(assistant_manager_settings.assistant_manager_grpc_addr)

        logger.info(f'starting gRPC server on {assistant_manager_settings.assistant_manager_grpc_addr}')
        await server.start()
        await server.wait_for_termination()

    def _create_event_loop(self, task):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(task())
        return

    async def run(self):
        processes = [
            Process(target=self._create_event_loop, args=(self.run_grpc_server,)),
            Process(target=self._create_event_loop, args=(self.run_bot,)),
        ]
        for process in processes:
            process.start()

        for process in processes:
            process.join()
