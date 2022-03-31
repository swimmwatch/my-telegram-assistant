"""
Init Celery application.
"""
import os

from celery import Celery
from dependency_injector.wiring import inject, Provide
from pytube import YouTube

from services.assistant.assistant_pb2 import SendTextRequest
from services.assistant.grpc_client import AssistantGrpcClient
# from services.worker.config import BROKER_URL, BACKEND_URL
from services.worker.container import WorkerContainer

celery = Celery(broker='redis://redis', backend='redis://redis')


@celery.on_after_configure.connect
def init_di_container(sender, **kwargs):
    worker_container = WorkerContainer()
    worker_container.wire(modules=[__name__])


@celery.task
@inject
def download_and_send_youtube_video(
        chat_id: int,
        link: str,
        assistant_grpc_client: AssistantGrpcClient = Provide[WorkerContainer.assistant_grpc_client]
):
    yt = YouTube(link)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
    out_dir = os.path.join('/tmp', 'youtube')
    out_filename = yt.video_id
    stream.download(out_dir, out_filename)
    video_path = os.path.join(out_dir, out_filename)

    req = SendTextRequest(chat_id=chat_id, text=video_path, disable_notification=True)
    assistant_grpc_client.client.send_text(req)
