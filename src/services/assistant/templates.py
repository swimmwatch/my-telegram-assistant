"""
Assistant service template utilities.
"""
from services.assistant.config import AssistantSettings
from utils.telegram.templates import render_template

settings = AssistantSettings()  # type: ignore


def render_template_(template_name: str, data: dict | None = None) -> str:
    return render_template(settings.template_dir, template_name, data)


def render_error(content: str) -> str:
    return render_template_("error/inline.html", {"content": content})
