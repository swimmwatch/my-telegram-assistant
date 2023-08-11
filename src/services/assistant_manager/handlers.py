"""
Assistant manager handlers.
"""
import grpc
from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from google.protobuf.empty_pb2 import Empty
from loguru import logger
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Update
from telegram import WebAppInfo
from telegram.ext import ContextTypes

from services.assistant.grpc_.client import AssistantGrpcClient
from services.assistant_manager.config import AssistantManagerSettings
from services.assistant_manager.container import AssistantManagerContainer
from utils.python_telegram_bot.decorators import serve_only_specific_user

assistant_manager_settings = AssistantManagerSettings()  # type: ignore
serve_only_me = serve_only_specific_user(assistant_manager_settings.my_telegram_id)


@serve_only_me
@inject
async def handle_login_request(
    update: Update,
    _: ContextTypes.DEFAULT_TYPE,
    assistant_grpc_client: AssistantGrpcClient = Provide[AssistantManagerContainer.assistant_grpc_client],
):
    req = Empty()
    try:
        assistant_grpc_client.stub.authorize_user(req)
    except grpc.RpcError as err:
        status_code = err.code()
        detail_msg = err.details()
        match status_code:
            case grpc.StatusCode.ALREADY_EXISTS:
                await update.message.reply_text(detail_msg)  # type: ignore
            case _:
                logger.error(detail_msg)
                await update.message.reply_text("Something went wrong.")  # type: ignore


@serve_only_me
@inject
async def handle_logout_request(
    update: Update,
    _: ContextTypes.DEFAULT_TYPE,
    assistant_grpc_client: AssistantGrpcClient = Provide[AssistantManagerContainer.assistant_grpc_client],
):
    req = Empty()
    try:
        assistant_grpc_client.stub.logout_user(req)
    except grpc.RpcError as err:
        status_code = err.code()
        detail_msg = err.details()
        match status_code:
            case grpc.StatusCode.UNAUTHENTICATED:
                await update.message.reply_text(detail_msg)  # type: ignore
            case _:
                logger.error(detail_msg)
                await update.message.reply_text("Something went wrong.")  # type: ignore
    else:
        await update.message.reply_text("You logged out.")  # type: ignore


@serve_only_me
@inject
async def handle_status_request(
    update: Update,
    _: ContextTypes.DEFAULT_TYPE,
    assistant_grpc_client: AssistantGrpcClient = Provide[AssistantManagerContainer.assistant_grpc_client],
):
    req = Empty()
    res = assistant_grpc_client.stub.is_user_authorized(req)
    if res.value:
        await update.message.reply_text("You are authorized.")  # type: ignore
    else:
        await update.message.reply_text("You are not authorized.")  # type: ignore


@serve_only_me
@inject
async def handle_settings_request(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    settings = AssistantManagerSettings()  # type: ignore
    web_app_info = WebAppInfo(url=settings.telegram_bot_webapp_url)
    keyboard = [
        [
            InlineKeyboardButton("Open assistant settings", web_app=web_app_info),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = update.message
    if message:
        await message.reply_text(
            "Please press the button below to setup assistant settings via the WebApp.",
            reply_markup=reply_markup,
        )
