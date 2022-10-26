"""
Assistant manager service entrypoint.
"""
import asyncio
from multiprocessing import Process

from grpc import aio
from loguru import logger
from telegram.ext import Application, CommandHandler

from services.assistant_manager import assistant_manager_pb2_grpc
from services.assistant_manager.config import assistant_manager_settings
from services.assistant_manager.grpc.server import AsyncAssistantManagerService
from services.assistant_manager.handlers import (
    handle_login_request,
    handle_logout_request,
    handle_status_request,
    handle_settings_request,
)


class AssistantManagerEntrypoint:
    def __init__(self, telegram_bot_token: str):
        self._app = Application.builder().token(telegram_bot_token).build()
        self._bot = self._app.bot

    def _setup_bot_handlers(self):
        self._app.add_handlers(
            [
                CommandHandler("start", handle_login_request),
                CommandHandler("stop", handle_logout_request),
                CommandHandler("status", handle_status_request),
                CommandHandler("settings", handle_settings_request),
            ]
        )

    def _run_bot(self):
        self._setup_bot_handlers()

        logger.info("launch bot")
        self._app.run_polling()

    async def _run_grpc_server(self):
        server = aio.server()
        assistant_manager_pb2_grpc.add_AssistantManagerServicer_to_server(
            AsyncAssistantManagerService(self._bot), server
        )
        server.add_insecure_port(assistant_manager_settings.assistant_grpc_addr)

        logger.info(
            f"starting gRPC server on {assistant_manager_settings.assistant_grpc_addr}"
        )
        await server.start()
        await server.wait_for_termination()

    def _create_event_loop(self, task):
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(task())
        return

    def run(self):
        """
        Run assistant manager service.
        """
        processes = (
            Process(target=self._create_event_loop, args=(self._run_grpc_server,)),
            Process(target=self._run_bot),
        )
        for process in processes:
            process.start()

        for process in processes:
            process.join()
