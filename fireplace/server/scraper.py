import aiohttp
from .. import logger


class Scraper:

    @staticmethod
    async def read_sensor(target: str) -> dict:
        """ Retrieve sensor data from a target (IPv4, IPv6 or DNS)

        @param target: Target address
        @returns: {temperature: ...}
        """
        async with aiohttp.ClientSession() as sess:
            async with sess.get(target) as resp:
                return await resp.json()
