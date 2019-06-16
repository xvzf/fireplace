import asyncio
import signal
import functools
import aiohttp
from pprint import pprint
from . import logger, load_config, Config
from .scraper import Scraper
from .scheduler import AsyncScheduler


def teardown():
    """ Safely teardown all running coroutines """
    logger.info("Stop signal, canceling all coroutines")
    for t in asyncio.Task.all_tasks():
        t.cancel()
    logger.info("Canceled all running coroutines")
    asyncio.get_event_loop().stop()
    logger.info("Eventloop stopped")


def get_scrape(target: str):
    """ Dummy scraper """
    async def scrape():
        try:
            t = await Scraper.read_sensor(target)
            logger.info(f"{t}")
        except:
            logger.warning(f"Could not retrieve data from {target}")

    return scrape


async def main(config: Config):
    """ Main entrypoint, creates all coroutines and returns """
    s = AsyncScheduler(loop=asyncio.get_event_loop())
    for target in config.targets:
        s.schedule_every(config.scrape_interval, get_scrape(target))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGHUP, teardown)
    loop.add_signal_handler(signal.SIGTERM, teardown)
    loop.create_task(main(load_config("test.yaml")))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        teardown()
