"""
Assistant manager entrypoint.
"""
import asyncio

import grpc
from aiogram import types
from dependency_injector.wiring import inject, Provide
from google.protobuf.empty_pb2 import Empty
from grpc import StatusCode
from loguru import logger

from services.assistant.grpc.client import AssistantGrpcClient
from services.assistant_manager.bot import dp
from services.assistant_manager.config import assistant_manager_settings
from services.assistant_manager.container import AssistantManagerContainer
from services.assistant_manager.entrypoint import AssistantManagerEntrypoint
from utils.aiogram.decorators import serve_only_specific_user

serve_only_me = serve_only_specific_user(assistant_manager_settings.my_telegram_id)


@dp.message_handler(commands=['start'])
@serve_only_me
@inject
async def handle_login_request(
        message: types.Message,
        assistant_grpc_client: AssistantGrpcClient = Provide[AssistantManagerContainer.assistant_grpc_client]
):
    req = Empty()
    try:
        assistant_grpc_client.stub.authorize_user(req)
    except grpc.RpcError as err:
        status_code = err.code()
        detail_msg = err.details()
        match status_code:
            case StatusCode.ALREADY_EXISTS:
                await message.answer(detail_msg)
            case _:
                logger.error(detail_msg)
                await message.answer('Something went wrong.')


@dp.message_handler(commands=['stop'])
@serve_only_me
@inject
async def handle_logout_request(
        message: types.Message,
        assistant_grpc_client: AssistantGrpcClient = Provide[AssistantManagerContainer.assistant_grpc_client]
):
    req = Empty()
    try:
        assistant_grpc_client.stub.logout_user(req)
    except grpc.RpcError as err:
        status_code = err.code()
        detail_msg = err.details()
        match status_code:
            case StatusCode.UNAUTHENTICATED:
                await message.answer(detail_msg)
            case _:
                logger.error(detail_msg)
                await message.answer('Something went wrong.')
    else:
        await message.answer('You logged out.')


@dp.message_handler(commands=['status'])
@serve_only_me
@inject
async def handle_status_request(
        message: types.Message,
        assistant_grpc_client: AssistantGrpcClient = Provide[AssistantManagerContainer.assistant_grpc_client]
):
    logger.info('call status handler')
    req = Empty()
    res = assistant_grpc_client.stub.is_user_authorized(req)
    if res.value:
        await message.answer('You are authorized.')
    else:
        await message.answer('You are not authorized.')


async def main():
    assistant_manager_container = AssistantManagerContainer()
    assistant_manager_container.wire(modules=[__name__])

    # assistant_manager_entrypoint = assistant_manager_container.assistant_manager_entrypoint()
    assistant_manager_entrypoint = AssistantManagerEntrypoint(dp)

    await assistant_manager_entrypoint.run()


if __name__ == '__main__':
    asyncio.run(main())
