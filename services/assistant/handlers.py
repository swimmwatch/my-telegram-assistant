import functools
from enum import Enum
from typing import NamedTuple

from loguru import logger
from htmgem.tags import a

from services.assistant.commands import CommandRequest, ExplicitCommand, ParsedArguments, ExplicitCommandHandler
from services.worker.app import download_and_send_post
from utils.common.patterns import AsyncChainOfResponsibility
from utils.post.impl import YouTubeShortVideo
from utils.youtube import extract_youtube_link


class YouTubeShortVideoDownloadCommandHandler(AsyncChainOfResponsibility):
    async def process_request(self, request: CommandRequest) -> bool:
        if not request.text:
            return False

        link = extract_youtube_link(request.text)
        if not link:
            return False

        # remove web page preview
        if not request.replied:
            await request.client.edit_text(
                request.message.chat_id,
                request.message.id,
                text=request.text,
                disable_web_page_preview=True
            )

        post = YouTubeShortVideo(link)
        download_and_send_post.delay(request.message.chat_id, post.id)
        logger.info(f'downloading YouTube short video post: {link}')

        return True


class TypeProfiles(Enum):
    WORK = 'work'
    GAME = 'game'


class WorkScopeValues(Enum):
    EMAIL = 'email'
    CV = 'cv'
    GITHUB = 'github'
    LINKEDIN = 'linkedin'
    TELEGRAM = 'telegram'


class GameScopeValues(Enum):
    ORIGIN = 'origin'
    EPIC = 'epic'
    STEAM = 'steam'
    DISCORD = 'discord'
    PSN = 'psn'
    UBISOFT = 'ubisoft'


class ScopeInfo(NamedTuple):
    full_name: str
    value: str


about_me_command = ExplicitCommand(name="me").add_arg(name='type', type_=TypeProfiles).add_arg(name='scope', type_=str)

work_info_dict = {
    WorkScopeValues.EMAIL: ScopeInfo(
        full_name="\N{CLOSED MAILBOX WITH RAISED FLAG} Email",
        value=a(
            {
                'href': 'mailto:contact.vasiliev.dmitry@gmail.com'
            }, "contact.vasiliev.dmitry@gmail.com"
        )
    ),
    WorkScopeValues.CV: ScopeInfo(
        full_name='\N{SCROLL} CV',
        value=f"{a({'href': 'www.example.com'}, 'Russian version')},"  # TODO: add short link
              f" {a({'href': 'www.example.com'}, 'English version')}"  # TODO: add short link
    ),
    WorkScopeValues.GITHUB: ScopeInfo(
        full_name='\N{GLOBE WITH MERIDIANS} GitHub',
        value=f"{a({'href': 'https://github.com/swimmwatch'}, 'swimmwatch')}"
    ),
    WorkScopeValues.LINKEDIN: ScopeInfo(
        full_name='\N{BRIEFCASE} LinkedIn',
        value=f"{a({'href': 'https://www.linkedin.com/in/dmitry-vasiliev/?locale=ru_RU'}, 'Russian version')},"
              f" {a({'href': 'https://www.linkedin.com/in/dmitry-vasiliev'}, 'English version')}"
    ),
    WorkScopeValues.TELEGRAM: ScopeInfo(
        full_name='\N{TELEPHONE RECEIVER} Telegram',
        value="@contact_dmitry_vasiliev"
    ),
}


@about_me_command.on(lambda args: args['type'] is TypeProfiles.WORK)
async def handle_output_work_profile(args: ParsedArguments, request: CommandRequest):
    if args['scope'] is None:
        header = 'My business card: \n'
        info_items_text = \
            '\n'.join(
                f'\N{BULLET} {info.full_name}: {info.value}'
                for info in work_info_dict.values()
            )
        res_message = header + info_items_text
    else:
        scope_value = WorkScopeValues(args['scope'])
        work_item = work_info_dict.get(scope_value, None)

        if work_item is None:
            # TODO: handle error through Telegram bot
            return

        res_message = f'{work_item.full_name}: {work_item.value}'

    await request.client.send_text(
        request.message.chat_id,
        res_message,
        disable_web_page_preview=True
    )


game_info_dict = {
    GameScopeValues.PSN: ScopeInfo(
        full_name='Playstation Network',
        value=a(
            {
                # TODO: fina another link
                'href': 'https://www.exophase.com/psn/user/swimmwatch/'
            },
            'swimmwatch'
        )
    ),
    GameScopeValues.EPIC: ScopeInfo(
        full_name='Epic Games',
        value=a(
            {
                # TODO: fina another link
                'href': 'https://www.exophase.com/epic/user/swimmwatch/'
            },
            'swimmwatch'
        )
    ),
    GameScopeValues.STEAM: ScopeInfo(
        full_name='Steam',
        value=a(
            {
                'href': 'https://steamcommunity.com/profiles/76561198076339909'
            },
            'swimmwatch'
        )
    ),
    GameScopeValues.DISCORD: ScopeInfo(
        full_name='Discord',
        value=a(
            {
                'href': 'https://discordapp.com/users/277206963845201932'
            },
            'swimmwatch'
        )
    ),
    GameScopeValues.ORIGIN: ScopeInfo(
        full_name='Origin',
        value=a(
            {
                'href': 'https://www.exophase.com/origin/user/swimmwatch/'
            },
            'swimmwatch'
        )
    ),
    GameScopeValues.UBISOFT: ScopeInfo(
        full_name='Ubisoft Connect',
        value=a(
            {
                'href': 'https://www.exophase.com/uplay/user/swimmwatch007/'
            },
            'swimmwatch007'
        )
    )
}


@about_me_command.on(lambda args: args['type'] is TypeProfiles.GAME)
async def handle_output_game_profile(args: ParsedArguments, request: CommandRequest):
    if args['scope'] is None:
        header = '\N{VIDEO GAME} My game profiles \N{VIDEO GAME}: \n'
        info_items_text = \
            '\n'.join(
                f'\N{BULLET} {info.full_name}: {info.value}'
                for info in game_info_dict.values()
            )
        res_message = header + info_items_text
    else:
        scope_value = GameScopeValues(args['scope'])
        game_item = game_info_dict.get(scope_value, None)

        if game_item is None:
            # TODO: handle error through Telegram bot
            return

        res_message = f'{game_item.full_name}: {game_item.value}'

    await request.client.send_text(
        request.message.chat_id,
        res_message,
        disable_web_page_preview=True
    )


hello_command = ExplicitCommand(name="hello")


@hello_command.on()
async def handle_welcome_output(_: ParsedArguments, request: CommandRequest):
    project_link_html = a({'href': 'https://github.com/swimmwatch/my-telegram-assistant'}, 'Telegram Assistant')
    res_message = '\n'.join([
        f"Hi! This message was sent by \N{ROBOT FACE} {project_link_html}.",
        "In short, this program helps to automate messaging in Telegram."
    ])
    await request.client.send_text(
        request.message.chat_id,
        res_message
    )


async def serve_only_replied_request(func: ExplicitCommandHandler) -> ExplicitCommandHandler:
    """
    Decorate explicit command handler for handling only replied requests.

    :param func: Explicit command handler
    :return: Wrapped explicit command handler
    """
    @functools.wraps(func)
    async def wrapper(args: ParsedArguments, request: CommandRequest):
        reply_to_message_id = request.message.reply_to_message_id
        if reply_to_message_id:
            func(args, request)

    return wrapper


reply_download_post_command = ExplicitCommand(name="d")


@reply_download_post_command.on()
@serve_only_replied_request
async def handle_replied_download_post_call(_: ParsedArguments, request: CommandRequest):
    replied_message = await request.client.api.get_message(
        request.message.chat_id,
        request.message.reply_to_message_id
    )
    inner_req = CommandRequest(
        message=replied_message,
        client=request.client,
        replied=True
    )
    yt_handler = YouTubeShortVideoDownloadCommandHandler(None)
    await yt_handler.process_request(inner_req)


# class TikTokVideoDownloadCommandHandler(ChainOfResponsibility):
#     def process_request(self, request: CommandRequest) -> bool:
#         link = extract_tiktok_link(request.message)
#         if not link:
#             return False
#
#         post = TikTokVideo(link)
#         download_and_send_post.delay(request.chat_id, post.id)
#         logger.info(f'downloading TikTok post: {link}')
#
#         return True
