"""
"About me" command models.
"""
from enum import Enum

from htmgem.tags import a


class TypeProfiles(Enum):
    WORK = "work"
    GAME = "game"


class WorkScopeValues(Enum):
    EMAIL = "email"
    CV = "cv"
    GITHUB = "github"
    LINKEDIN = "linkedin"
    TELEGRAM = "telegram"


class GameScopeValues(Enum):
    ORIGIN = "origin"
    EPIC = "epic"
    STEAM = "steam"
    DISCORD = "discord"
    PSN = "psn"
    UBISOFT = "ubisoft"


work_info_dict = {
    WorkScopeValues.EMAIL: (
        "\N{CLOSED MAILBOX WITH RAISED FLAG} Email",
        a(
            {"href": "mailto:contact.vasiliev.dmitry@gmail.com"},
            "contact.vasiliev.dmitry@gmail.com",
        ),
    ),
    WorkScopeValues.CV: (
        "\N{SCROLL} CV",
        # TODO: add short link
        f"{a({'href': 'https://hh.ru/resume_converter/Васильев Дмитрий Олегович.pdf?hash=78777defff08eb88a60039ed1f6f7739383057&type=pdf&hhtmSource=resume&hhtmFrom=resume_list&force-roles=true'}, 'Russian version')},"  # noqa: E501
        f" {a({'href': 'www.linkedin.com/in/dmitry-vasiliev'}, 'English version')}",  # TODO: add short link
    ),
    WorkScopeValues.GITHUB: (
        "\N{GLOBE WITH MERIDIANS} GitHub",
        f"{a({'href': 'https://github.com/swimmwatch'}, 'swimmwatch')}",
    ),
    WorkScopeValues.LINKEDIN: (
        "\N{BRIEFCASE} LinkedIn",
        f"{a({'href': 'https://www.linkedin.com/in/dmitry-vasiliev/?locale=ru_RU'}, 'Russian version')},"
        f" {a({'href': 'https://www.linkedin.com/in/dmitry-vasiliev'}, 'English version')}",
    ),
    WorkScopeValues.TELEGRAM: ("\N{TELEPHONE RECEIVER} Telegram", "@contact_dmitry_vasiliev"),
}

game_info_dict = {
    GameScopeValues.PSN: (
        "Playstation Network",
        a(
            {
                # TODO: fina another link
                "href": "https://www.exophase.com/psn/user/swimmwatch/"
            },
            "swimmwatch",
        ),
    ),
    GameScopeValues.EPIC: (
        "Epic Games",
        a(
            {
                # TODO: fina another link
                "href": "https://www.exophase.com/epic/user/swimmwatch/"
            },
            "swimmwatch",
        ),
    ),
    GameScopeValues.STEAM: (
        "Steam",
        a(
            {"href": "https://steamcommunity.com/profiles/76561198076339909"},
            "swimmwatch",
        ),
    ),
    GameScopeValues.DISCORD: (
        "Discord",
        a({"href": "https://discordapp.com/users/277206963845201932"}, "swimmwatch"),
    ),
    GameScopeValues.ORIGIN: (
        "Origin",
        a({"href": "https://www.exophase.com/origin/user/swimmwatch/"}, "swimmwatch"),
    ),
    GameScopeValues.UBISOFT: (
        "Ubisoft Connect",
        a(
            {"href": "https://www.exophase.com/uplay/user/swimmwatch007/"},
            "swimmwatch007",
        ),
    ),
}
