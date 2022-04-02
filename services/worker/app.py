"""
Init Celery application.
"""
import pytube.exceptions
from celery import Celery
from dependency_injector.wiring import inject
from loguru import logger
from pytube import YouTube

from services.assistant.assistant_pb2 import SendVideoRequest
from services.assistant.grpc_client import AssistantGrpcClient
# TODO: use env variables for init Celery broker and backend
# from services.worker.config import BROKER_URL, BACKEND_URL
from services.worker.config import ASSISTANT_GRPC_ADDR, YT_MAX_VIDEO_LENGTH, YT_OUT_DIR
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
        # TODO: fix it
        # assistant_grpc_client: AssistantGrpcClient = Provide[WorkerContainer.assistant_grpc_client]
):
    try:
        yt = YouTube(link)
    except pytube.exceptions.VideoUnavailable:
        logger.info(f'{link}: video is unavailable')
        return

    if yt.length >= YT_MAX_VIDEO_LENGTH:
        logger.info(f'{link} video too long')
        return

    stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
    if stream is None:
        logger.warning(f'{link}: stream is not available')
        return

    out_filename = yt.video_id
    video_path = stream.download(YT_OUT_DIR, out_filename)

    assistant_grpc_client = AssistantGrpcClient(ASSISTANT_GRPC_ADDR)
    req = SendVideoRequest(
        chat_id=chat_id,
        video_path=video_path,
        caption=yt.title,
        disable_notification=True
    )
    assistant_grpc_client.stub.send_video(req)
