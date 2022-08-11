"""
Assistant manager entrypoint.
"""
import asyncio

from grpc import aio
from loguru import logger

from services.assistant_manager import assistant_manager_pb2_grpc
from services.assistant_manager.bot import dp, bot
from services.assistant_manager.config import assistant_manager_settings
from services.assistant_manager.grpc.server import AsyncAssistantManagerService
from utils.aiogram.decorators import serve_only_specific_user

serve_only_me = serve_only_specific_user(assistant_manager_settings.my_telegram_id)


async def run_grpc_server():
    server = aio.server()
    assistant_manager_pb2_grpc.add_AssistantManagerServicer_to_server(
        AsyncAssistantManagerService(bot),
        server
    )
    server.add_insecure_port(assistant_manager_settings.assistant_manager_grpc_addr)

    logger.info(f'starting gRPC server on {assistant_manager_settings.assistant_manager_grpc_addr}')
    await server.start()
    await server.wait_for_termination()


async def run_bot():
    await dp.start_polling()


async def main():
    logger.info('launch bot')
    await asyncio.gather(
        run_grpc_server(),
        run_bot()
    )


if __name__ == '__main__':
    asyncio.run(main())
