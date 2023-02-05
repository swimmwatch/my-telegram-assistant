from datetime import datetime

from celery import shared_task
from dependency_injector.wiring import Provide, inject
from loguru import logger

from services.worker.config import OUT_DIR
from services.worker.container import WorkerContainer
from utils.post.cache.state import PostCacheState
from utils.post.exceptions import PostNonDownloadable, PostTooLarge, PostUnavailable
from utils.post.impl import PostFactory


@shared_task
@inject
def clear_cached_post(
    post_id: str,
    out_filename: str,
    post_state_cache_manager=Provide[WorkerContainer.post_cache_state_manager],
):
    """Clear cached post"""
    post = PostFactory.init_from_post_id(post_id)
    post_state_cache_manager.clear_state(post.id)
    post.clear(out_filename)


@shared_task
@inject
def download_and_send_post(
    chat_id: int,
    post_id: str,
    post_state_cache_manager=Provide[WorkerContainer.post_cache_state_manager],
    assistant_grpc_client=Provide[WorkerContainer.assistant_grpc_client],
):
    try:
        post = PostFactory.init_from_post_id(post_id)
    except (PostUnavailable, PostTooLarge) as err:
        logger.info(err.message)
        return

    cache_state, filename = post_state_cache_manager.get_state(post.id)
    if cache_state is PostCacheState.NONE:
        try:
            out_filename = post.download(OUT_DIR)
        except PostNonDownloadable as err:
            logger.warning(err.message)
            return
        post_state_cache_manager.set_state(
            post.id, PostCacheState.DOWNLOADED, out_filename
        )
    elif cache_state is PostCacheState.DOWNLOADED and filename:
        out_filename = filename

    post.send(
        assistant_grpc_client,
        video_path=out_filename,
        chat_id=chat_id,
        disable_notification=True,
    )

    release_date = datetime.now() + post.ttl
    clear_cached_post.apply_async((post.id, out_filename), eta=release_date)
