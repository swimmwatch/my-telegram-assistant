"""
Command for mentioning all in basic chat.
"""
from services.assistant.commands import CommandRequest, ExplicitCommand, ParsedArguments
from services.assistant.commands.decorators import serve_only_group_messages
from utils.telegram.message import get_mention_text

all_command = ExplicitCommand(name="all")


@all_command.on()
@serve_only_group_messages
async def handle_all_command(_: ParsedArguments, request: CommandRequest):
    me = await request.event.client.get_me()
    my_id = me.id
    members = request.event.client.iter_participants(request.event.message.chat_id, aggressive=True)
    mentions = [
        get_mention_text(member.id, member.username)
        async for member in members
        if not member.bot and member.username and member.id != my_id
    ]
    mention_msg = ", ".join(mentions)
    await request.event.client.send_message(request.event.message.chat_id, mention_msg, parse_mode="html")
