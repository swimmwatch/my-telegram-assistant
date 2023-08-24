from dependency_injector.wiring import Provide
from dependency_injector.wiring import inject
from google.protobuf.empty_pb2 import Empty
from telegram import Update
from telegram.ext import ContextTypes

from services.assistant.grpc_.client import AssistantAsyncGrpcClient
from services.bot.container import TelegramBotContainer
from services.bot.permissions import registered
from services.db import models


@registered
@inject
async def handle_status_request(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    current_user: models.User,
    assistant_grpc_client: AssistantAsyncGrpcClient = Provide[TelegramBotContainer.assistant_grpc_client],
):
    request = Empty()
    response = await assistant_grpc_client.stub.is_authorized(request)
    is_authorized = response.value
    if is_authorized:
        await update.message.reply_text("You are authorized.")  # type: ignore
    else:
        await update.message.reply_text("You are not authorized.")  # type: ignore
