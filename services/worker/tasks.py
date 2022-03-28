import os

from asgiref.sync import async_to_sync
from pytube import YouTube

from services.assistant.utils.message import send_video
from services.worker.app import celery


@celery.task
def download_and_send_youtube_video(chat_id: int, link: str):
    yt = YouTube(link)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('res').desc().first()
    out_dir = os.path.join('/tmp', 'youtube')
    out_filename = yt.video_id
    stream.download(out_dir, out_filename)
    video_path = os.path.join(out_dir, out_filename)
    async_to_sync(send_video)(chat_id, video_path)
