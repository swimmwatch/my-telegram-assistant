"""
Hello command handler.
"""
from htmgem.tags import a

from services.assistant.commands import ExplicitCommand, ParsedArguments, CommandRequest

hello_command = ExplicitCommand(name="hello")


@hello_command.on()
async def handle_welcome_output(_: ParsedArguments, request: CommandRequest):
    project_link_html = a({'href': 'https://github.com/swimmwatch/my-telegram-assistant'}, 'Telegram Assistant')
    user_info = await request.client.get_user(request.message.chat_id)
    username = user_info.username
    if not username:
        username = f'{user_info.first_name} {user_info.last_name}'
    res_message = '\n'.join([
        f"Hi, {username}! This message was sent by \N{ROBOT FACE} {project_link_html}.",
        "In short, this program helps to automate messaging in Telegram."
    ])
    await request.client.send_text(
        request.message.chat_id,
        res_message
    )
