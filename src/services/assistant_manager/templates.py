"""
Assistant service template utilities.
"""
from services.assistant_manager.config import AssistantManagerSettings
from utils.telegram.templates import render_template

settings = AssistantManagerSettings()  # type: ignore


def render_template_(template_name: str, data: dict | None = None) -> str:
    return render_template(settings.template_dir, template_name, data)


def render_error(content: str) -> str:
    return render_template_("error/inline.html", {"content": content})
