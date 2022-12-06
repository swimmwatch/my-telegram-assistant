"""
Assistant manager entrypoint.
"""
from services.assistant_manager.config import assistant_manager_settings
from services.assistant_manager.container import AssistantManagerContainer
from services.assistant_manager.entrypoint import AssistantManagerEntrypoint


def main():
    assistant_manager_container = AssistantManagerContainer()
    assistant_manager_container.wire(modules=[__name__, ".handlers"])

    assistant_manager_entrypoint = AssistantManagerEntrypoint(
        assistant_manager_settings.telegram_api_token
    )

    assistant_manager_entrypoint.run()


if __name__ == "__main__":
    main()
