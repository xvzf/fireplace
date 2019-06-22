import http3
import json
from .. import logger


class ScrapeException(Exception):
    pass


class Scraper:

    @staticmethod
    async def read_sensor(target: str) -> dict:
        """ Retrieve sensor data from a target (IPv4, IPv6 or DNS)

        @param target: Target address
        @returns: {temperature: ...}
        """
        async with http3.AsyncClient() as client:
            try:
                resp = await client.get(target)
                if resp.status_code != 200:
                    raise ScrapeException
                return json.loads(resp.text)
            except ConnectionRefusedError:
                raise ScrapeException