"""
Assistant manager entrypoint.
"""
from services.bot.config import TelegramBotSettings
from services.bot.container import TelegramBotContainer
from services.bot.entrypoint import TelegramBotEntrypoint


def main():
    container = TelegramBotContainer()
    container.wire(
        modules=[__name__],
        packages=["services.bot.handlers"],
    )
    telegram_bot_settings = TelegramBotSettings()

    telegram_bot_entrypoint = TelegramBotEntrypoint(
        telegram_bot_settings.grpc_addr,
        telegram_bot_settings.token.get_secret_value(),
    )
    telegram_bot_entrypoint.run()


if __name__ == "__main__":
    main()
