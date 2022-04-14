from typing import Protocol

from services.assistant.assistant_pb2 import MessageResponse
from services.assistant.grpc_client import AssistantGrpcClient


class SupportsTelegramSending(Protocol):
    """
    Declares sending process to Telegram
    """
    def send(self, client: AssistantGrpcClient, **kwargs) -> MessageResponse:
        """
        Send data as Telegram message.

        :param client: Telegram client
        :param kwargs: Any arguments
        :return: Message response
        """
        ...
