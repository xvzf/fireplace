import asyncio
import signal
import functools
import aiohttp
from sanic import Sanic
from pprint import pprint
from . import logger, load_config, Config, Target
from .scraper import Scraper
from .scheduler import AsyncScheduler

app = Sanic(__name__)


def get_scrape(target: Target):
    """ Dummy scraper """
    async def scrape():
        try:
            t = await Scraper.read_sensor(target.url)
            logger.info(f"{t}")
        except:
            logger.warning(f"Could not retrieve data from {target}")

    return scrape


@app.listener("before_server_start")
async def setup_fireplace(app, loop):
    """ Main entrypoint, creates all coroutines and returns """
    config = load_config("test.yaml")
    s = AsyncScheduler(loop=loop)
    for target in config.targets:
        s.schedule_every(config.scrape_interval, get_scrape(target))


if __name__ == "__main__":
    app.run("::", port=8080)
