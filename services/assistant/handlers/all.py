"""
Command for mentioning all in basic chat.
"""
from services.assistant.commands import ExplicitCommand, CommandRequest, ParsedArguments
from services.assistant.commands.decorators import serve_only_basic_group_messages
from utils.aiotdlib.message import get_mention_text

all_command = ExplicitCommand(name='all')


@all_command.on()
@serve_only_basic_group_messages
async def handle_all_command(_: ParsedArguments, request: CommandRequest):
    chat_info = await request.client.get_chat_info(request.message.chat_id, full=True)
    members = chat_info.members
    mentions = []
    for member in members:
        member_id = member.member_id.user_id
        member_info = await request.client.get_user(member_id)
        mention = get_mention_text(member_id, member_info.username)
        mentions.append(mention)

    mention_msg = ', '.join(mentions)
    await request.client.send_text(request.message.chat_id, mention_msg)
