"""
Assistant.
"""
from telethon import TelegramClient
from telethon import events
from telethon.sessions import Session
from telethon.sessions import StringSession
from telethon.tl.types import User as TelethonUser

from services.assistant.commands.request import CommandRequest
from services.assistant.handlers import command_processor


class AssistantClient:
    def __init__(self, api_id: str, api_hash: str):
        self._api_id = api_id
        self._api_hash = api_hash
        self.telegram_client: TelegramClient | None = None

    async def log_out(self) -> bool:
        # TODO: handle case if telegram client is not exists
        status = await self.telegram_client.log_out()
        if status:
            self.telegram_client = None
        return status

    def client_factory(self, session: Session) -> None:
        # TODO: handle case if telegram client exists
        self.telegram_client = TelegramClient(
            session=session,
            api_id=self._api_id,
            api_hash=self._api_hash,
        )

    async def connect(self) -> None:
        # TODO: handle case if telegram client is not exists
        await self.telegram_client.connect()

    async def get_me(self) -> TelethonUser:
        # TODO: handle case if telegram client is not exists
        return await self.telegram_client.get_me()

    def get_session(self) -> str:
        # TODO: handle case if telegram client is not exists
        return StringSession.save(self.telegram_client.session)

    def _add_handlers(self):
        """
        Add Telegram handlers.
        """

        @self.telegram_client.on(events.NewMessage(outgoing=True))
        async def handle_new_own_message(event: events.NewMessage.Event):
            request = CommandRequest(event)
            await command_processor.handle(request)

    async def is_authorized(self) -> bool:
        if self.telegram_client:
            return await self.telegram_client.is_user_authorized()
        return False

    async def init(self):
        """
        Assistant initialization.
        """
        self._add_handlers()
