"""
URL RegExp patterns.
"""
import re

YOUTUBE_LINK_PATTERN = re.compile(
    r'((?:https?:)?\/\/)?((?:www|m)\.)?'
    r'((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?'
)

TIKTOK_LINK_PATTERN = re.compile(
    r'(?x)'
    r'https?://'
    r'(?:'
    r'(?:www|m|vt)\.'
    r'(?:tiktok\.com)\/'
    r'(?:.+)'
    r'(?:\/)?'
    r'(?:\?.+=)?'
    r')'
    r'(?P<id>[\da-z]+)'
)
