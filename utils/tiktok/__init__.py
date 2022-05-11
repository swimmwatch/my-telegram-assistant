"""
TikTok utils.
"""
import re
from typing import Optional

from utils.url_patterns import TIKTOK_LINK_PATTERN


def extract_tiktok_link(text: str) -> Optional[str]:
    """
    Extract TikTok link from text.

    :param text: Some text
    :return: Extracted TikTok link
    """
    match = re.match(TIKTOK_LINK_PATTERN, text)
    if not match:
        return None
    link = match.group(0)
    return link
