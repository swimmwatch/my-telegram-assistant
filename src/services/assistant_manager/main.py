"""
Assistant manager entrypoint.
"""
from services.assistant_manager.config import AssistantManagerSettings
from services.assistant_manager.container import AssistantManagerContainer
from services.assistant_manager.entrypoint import AssistantManagerEntrypoint


def main():
    assistant_manager_settings = AssistantManagerSettings()
    assistant_manager_container = AssistantManagerContainer()
    assistant_manager_container.wire(modules=[__name__, ".handlers"])

    assistant_manager_entrypoint = AssistantManagerEntrypoint(
        assistant_manager_settings.telegram_api_token.get_secret_value()
    )

    assistant_manager_entrypoint.run()


if __name__ == "__main__":
    main()
