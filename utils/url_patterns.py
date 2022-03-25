"""
URL RegExp patterns.
"""
import re

YOUTUBE_LINK_PATTERN = re.compile(
    r'((?:https?:)?\/\/)?((?:www|m)\.)?'
    r'((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?'
)
