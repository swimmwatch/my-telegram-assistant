"""
Aiotdlib message utils.
"""
from htmgem.tags import a


def get_mention_text(user_id: int, username: str) -> str:
    """
    Return mention text

    :param user_id: User ID
    :param username: Username
    :return: Message text with mention
    """
    return a({'href': f'tg://user?id={user_id}'}, username)
