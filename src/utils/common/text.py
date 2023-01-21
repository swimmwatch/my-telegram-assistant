"""
Text manipulation helpers.
"""
import re

RE_HASHTAG = re.compile(r"(#[\w]+)")


def remove_hashtags(text: str) -> str:
    """
    Remove hashtags from text
    :param text: Some string
    :return: String without hashtags
    """
    res = re.sub(RE_HASHTAG, "", text)
    return res
