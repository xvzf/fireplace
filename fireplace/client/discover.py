import asyncio
import http3
import json
from .. import config
from . import logger


async def get_config(url: str) -> config.Target:
    """ Retrieves the configuration from a remote server """
    async with http3.AsyncClient() as client:
        while True:
            try:
                resp = await client.get(url)
                return config.Target(**json.loads(resp.text))
            except Exception as e:
                logger.exception(e)
                await asyncio.sleep(1)