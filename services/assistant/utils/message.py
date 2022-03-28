"""
Assistant helpers for messaging.
"""
from services.assistant import aiotdlib_client


async def send_video(chat_id: int, video_path: str) -> None:
    """
    Send video using assistant service client
    :param chat_id: Chat ID
    :param video_path: Path to video file
    """
    await aiotdlib_client.send_video(chat_id, video_path)
