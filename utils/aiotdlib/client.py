"""
Custom clients for Aiotdlib.
"""
import asyncio

import aiotdlib
from loguru import logger
from redis import Redis
from dependency_injector.wiring import inject, Provide

from app.container import Container


class CustomClient(aiotdlib.Client):
    @inject
    async def _auth_get_code(self, redis_client: Redis = Provide[Container.redis_client]) -> str:
        code = None
        key_auth_code = 'auth_code'
        logger.info('start polling auth code')
        while not code:
            code = redis_client.get(key_auth_code)
            if not code:
                logger.info('current code is none')
            else:
                code = code.decode()
            await asyncio.sleep(5)

        redis_client.delete(key_auth_code)

        logger.info(f'got auth code: {code}')  # TODO: remove auth code from logs
        return code
