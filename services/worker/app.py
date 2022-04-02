"""
Init Celery application.
"""
import os.path
from datetime import datetime, timedelta
from pathlib import Path

import pytube.exceptions
from celery import Celery
from dependency_injector.wiring import inject, Provide
from loguru import logger
from pytube import YouTube
from redis import Redis

from services.assistant.assistant_pb2 import SendVideoRequest, ForwardMessagesRequest
from services.assistant.grpc_client import AssistantGrpcClient
# TODO: use env variables for init Celery broker and backend
# from services.worker.config import BROKER_URL, BACKEND_URL
from services.worker.config import ASSISTANT_GRPC_ADDR, YT_MAX_VIDEO_LENGTH, YT_OUT_DIR, YT_VIDEO_TTL
from services.worker.container import WorkerContainer

celery = Celery(broker='redis://redis', backend='redis://redis')


@celery.on_after_configure.connect
def init_di_container(sender, **kwargs):
    worker_container = WorkerContainer()
    worker_container.wire(modules=[__name__])


@celery.task
def clear_cache_youtube_video(video_path: Path):
    """Clear YouTube video from cache"""
    if os.path.exists(video_path):
        os.remove(video_path)


@celery.task
@inject
def download_and_send_youtube_video(
        chat_id: int,
        link: str,
        redis_client: Redis = Provide[WorkerContainer.redis_client]
        # TODO: fix it
        # assistant_grpc_client: AssistantGrpcClient = Provide[WorkerContainer.assistant_grpc_client]
):
    assistant_grpc_client = AssistantGrpcClient(ASSISTANT_GRPC_ADDR)

    try:
        yt = YouTube(link)
    except pytube.exceptions.VideoUnavailable:
        logger.info(f'{link}: video is unavailable')
        return

    if yt.length >= YT_MAX_VIDEO_LENGTH:
        logger.info(f'{link} video too long')
        return

    # forward message if it's existing in cache
    yt_cached_msg_id = f'youtube:{yt.video_id}'
    if redis_client.exists(yt_cached_msg_id):
        chat_message_id = redis_client.get(yt_cached_msg_id).decode()
        from_chat_id, message_id = map(int, chat_message_id.split(':'))
        req = ForwardMessagesRequest(
            from_chat_id=from_chat_id,
            chat_id=chat_id,
            disable_notification=True
        )
        req.message_ids.append(message_id)
        assistant_grpc_client.stub.forward_messages(req)
        return

    stream = yt.streams.filter(progressive=True, file_extension='mp4').get_highest_resolution()
    if stream is None:
        logger.warning(f'{link}: stream is not available')
        return

    out_filename = yt.video_id
    video_path = stream.download(YT_OUT_DIR, out_filename)

    req = SendVideoRequest(
        chat_id=chat_id,
        video_path=video_path,
        caption=yt.title,
        disable_notification=True
    )
    result_msg = assistant_grpc_client.stub.send_video(req)

    video_ttl = timedelta(seconds=YT_VIDEO_TTL)
    # cache message id in Redis store
    redis_client.set(yt_cached_msg_id, f'{chat_id}:{result_msg.id}', video_ttl)

    release_date = datetime.now() + video_ttl
    clear_cache_youtube_video.apply_async((video_path,), eta=release_date)
