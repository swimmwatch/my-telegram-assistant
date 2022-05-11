from typing import Optional

from utils.url_patterns import YOUTUBE_LINK_PATTERN


def extract_youtube_link(msg: str) -> Optional[str]:
    """
    Extract link from text message.
    :param msg: Some message
    :return: Link
    """
    match = YOUTUBE_LINK_PATTERN.search(msg)
    if not match:
        return None
    link = match.group(0)
    return link
