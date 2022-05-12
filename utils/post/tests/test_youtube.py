"""
Unittests for YouTube posts.
"""
from os import path

import pytest

from utils.post.impl import YouTubeShortVideo


@pytest.mark.smoke
def test_download_youtube_short_video_post():
    # download random video and delete it
    url = 'https://www.youtube.com/watch?v=jNQXAC9IVRw'
    yt = YouTubeShortVideo(url)
    out_dir = path.join('/tmp', 'data')
    expected_filename = path.join(out_dir, yt.id)
    out_filename = yt.download(out_dir)

    assert path.exists(out_filename)
    assert expected_filename == out_filename

    yt.clear(out_filename)
    assert not path.exists(out_filename)
