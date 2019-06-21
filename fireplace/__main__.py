import asyncio
import functools
from sanic import Sanic
from sanic_openapi import swagger_blueprint
from .scraper import Scraper
from .scheduler import AsyncScheduler
from .api import api_v1 as api
from .database import MetricDAO, initialize_db
from . import logger, load_config, Config, Target

app = Sanic(__name__)
app.register_blueprint(api)
app.register_blueprint(swagger_blueprint)


def get_scrape(app: Sanic, target: Target):
    """ Creates a scrape function which retrieves data from a specific
    target and adds the datapoint to the database :-)
    """
    async def scrape():
        try:
            data = await Scraper.read_sensor(target.url)
            await MetricDAO.add_now(app.db, target.name, data["temperature"])
            logger.info(f"{target}: {data}")
        except Exception as e:
            logger.exception(e)

            logger.warning(f"Could not retrieve data from {target}")
    return scrape


@app.listener("before_server_start")
async def setup_fireplace(app, loop):
    """ Main entrypoint, creates all coroutines and returns """
    config = load_config("test.yaml")
    await initialize_db(app, **config.database)

    s = AsyncScheduler(loop=loop)
    for target in config.targets:
        s.schedule_every(config.scrape_interval, get_scrape(app, target))


if __name__ == "__main__":
    app.run("::", port=8080)
