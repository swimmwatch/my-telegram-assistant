"""
Hello command handler.
"""
from htmgem.tags import a

from services.assistant.commands import CommandRequest, ExplicitCommand, ParsedArguments

hello_command = ExplicitCommand(name="hello")


@hello_command.on()
async def handle_welcome_output(_: ParsedArguments, request: CommandRequest):
    project_link_html = a(
        {"href": "https://github.com/swimmwatch/my-telegram-assistant"},
        "Telegram Assistant",
    )
    res_message = "\n".join(
        [
            f"Hi! This message was sent by \N{ROBOT FACE} {project_link_html}.",
            "In short, this program helps to automate messaging in Telegram.",
        ]
    )
    await request.event.client.send_message(request.event.message.chat_id, res_message, parse_mode="html")
