"""
Init Celery application.
"""
from datetime import datetime
from os import path

from celery import Celery
from dependency_injector.wiring import inject, Provide
from loguru import logger

from services.assistant.grpc.client import AssistantGrpcClient
from services.assistant.assistant_pb2 import ForwardMessagesRequest
from services.sent_post_msg_info_cache_manager import SentPostMessageInfoCacheManager
from services.worker.config import OUT_DIR, worker_settings
from services.worker.container import WorkerContainer
from utils.post.impl import PostFactory
from utils.post.cache.state import PostCacheState
from utils.post.cache.state.redis import RedisPostStateCacheManager
from utils.post.exceptions import PostNonDownloadable, PostUnavailable, PostTooLarge

celery = Celery(
    'tasks',
    broker=worker_settings.celery_broker_url,
    backend=worker_settings.celery_result_backend
)

task_routes = {
    'services.worker.app.download_and_send_post': {
        'queue': 'downloads'
    }
}


@celery.on_after_configure.connect
def init_di_container(sender, **kwargs):
    worker_container = WorkerContainer()
    worker_container.wire(modules=[__name__])


@celery.task
@inject
def clear_cached_post(
    post_id: str,
    out_filename: str,
    post_state_cache_manager: RedisPostStateCacheManager = Provide[WorkerContainer.post_cache_state_manager],
    sent_post_msg_info_cache_manager: SentPostMessageInfoCacheManager =
    Provide[WorkerContainer.sent_post_msg_info_cache_manager]
):
    """Clear cached post"""
    post = PostFactory.init_from_post_id(post_id)
    post_state_cache_manager.clear_state(post.id)
    sent_post_msg_info_cache_manager.clear_msg_info(post)
    post.clear(out_filename)


@celery.task
@inject
def download_and_send_post(
    chat_id: int,
    post_id: str,
    post_state_cache_manager: RedisPostStateCacheManager = Provide[WorkerContainer.post_cache_state_manager],
    sent_post_msg_info_cache_manager: SentPostMessageInfoCacheManager =
    Provide[WorkerContainer.sent_post_msg_info_cache_manager]
    # TODO: fix it
    # assistant_grpc_client: AssistantGrpcClient = Provide[WorkerContainer.assistant_grpc_client]
):
    assistant_grpc_client = AssistantGrpcClient(worker_settings.assistant_grpc_addr)

    try:
        post = PostFactory.init_from_post_id(post_id)
    except (PostUnavailable, PostTooLarge) as err:
        logger.info(err.message)
        return

    # forward message if it was sent
    msg_info = sent_post_msg_info_cache_manager.get_msg_info(post)
    if msg_info:
        req = ForwardMessagesRequest(
            from_chat_id=msg_info.chat_id,
            chat_id=chat_id,
            disable_notification=True
        )
        req.message_ids.append(msg_info.message_id)
        assistant_grpc_client.stub.forward_messages(req)
        return

    cache_state = post_state_cache_manager.get_state(post.id)
    if cache_state is PostCacheState.NONE:
        try:
            out_filename = post.download(OUT_DIR)
        except PostNonDownloadable as err:
            logger.warning(err.message)
            return
        post_state_cache_manager.set_state(post.id, PostCacheState.DOWNLOADED)
    elif cache_state is PostCacheState.DOWNLOADED:
        out_filename = path.join(OUT_DIR, post.id)

    result_msg = post.send(
        assistant_grpc_client,
        video_path=out_filename,
        chat_id=chat_id,
        disable_notification=True
    )

    # cache sent message with post
    sent_post_msg_info_cache_manager.cache_msg_info(chat_id, result_msg.id, post)

    release_date = datetime.now() + post.ttl
    clear_cached_post.apply_async((post.id, out_filename), eta=release_date)
