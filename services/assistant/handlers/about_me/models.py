"""
"About me" command models.
"""
from enum import Enum
from typing import NamedTuple

from htmgem.tags import a


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
