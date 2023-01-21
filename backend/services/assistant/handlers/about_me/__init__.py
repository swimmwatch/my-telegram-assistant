"""
"About me" command handler.
"""
from services.assistant.commands import CommandRequest, ExplicitCommand, ParsedArguments
from services.assistant.handlers.about_me.models import (
    GameScopeValues,
    TypeProfiles,
    WorkScopeValues,
    game_info_dict,
    work_info_dict,
)

about_me_command = (
    ExplicitCommand(name="me")
    .add_arg(name="type", type_=TypeProfiles)
    .add_arg(name="scope", type_=str)
)


@about_me_command.on(lambda args: args["type"] is TypeProfiles.WORK)
async def handle_output_work_profile(args: ParsedArguments, request: CommandRequest):
    if args["scope"] is None:
        header = "My business card: \n"
        info_items_text = "\n".join(
            f"\N{BULLET} {info.full_name}: {info.value}"
            for info in work_info_dict.values()
        )
        res_message = header + info_items_text
    else:
        scope_value = WorkScopeValues(args["scope"])
        work_item = work_info_dict.get(scope_value, None)

        if work_item is None:
            # TODO: handle error through Telegram bot
            return

        res_message = f"{work_item.full_name}: {work_item.value}"

    await request.event.client.send_message(
        request.event.message.chat_id, res_message, parse_mode="html", silent=True
    )


@about_me_command.on(lambda args: args["type"] is TypeProfiles.GAME)
async def handle_output_game_profile(args: ParsedArguments, request: CommandRequest):
    if args["scope"] is None:
        header = "\N{VIDEO GAME} My game profiles \N{VIDEO GAME}: \n"
        info_items_text = "\n".join(
            f"\N{BULLET} {info.full_name}: {info.value}"
            for info in game_info_dict.values()
        )
        res_message = header + info_items_text
    else:
        scope_value = GameScopeValues(args["scope"])
        game_item = game_info_dict.get(scope_value, None)

        if game_item is None:
            # TODO: handle error through Telegram bot
            return

        res_message = f"{game_item.full_name}: {game_item.value}"

    await request.event.client.send_message(
        request.event.message.chat_id, res_message, parse_mode="html", silent=True
    )
