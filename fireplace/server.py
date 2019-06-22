import asyncio
from sanic import Sanic
from sanic_openapi import swagger_blueprint

from .scraper import Scraper
from .database import MetricDAO, initialize_db
from . import logger, config
from .scheduler import AsyncScheduler

# Blueprint Endpoints
from .api import api
from .discovery import discovery


def get_scrape(app: Sanic, target: config.Target):
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


async def setup_server(app: Sanic, loop: asyncio.AbstractEventLoop):
    """ Main entrypoint, creates all coroutines and returns """
    config.load_config(app, "test.yaml")  # @TODO
    await initialize_db(app)

    # @TODO improve!
    s = AsyncScheduler(loop=loop)
    for target in app.fireplace.targets:
        s.schedule_every(app.fireplace.scrape_interval,
                         get_scrape(app, target))


def create_server():
    app = Sanic("fireplace_server")
    app.register_blueprint(api)
    app.register_blueprint(discovery)
    app.register_blueprint(swagger_blueprint)

    # Startup handler for fireplace server
    app.register_listener(setup_server, "before_server_start")

    return app
