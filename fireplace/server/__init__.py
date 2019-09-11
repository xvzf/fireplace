import os
import asyncio
from sanic import Sanic
from sanic.response import file
from sanic_openapi import swagger_blueprint

from .. import logger, config
from ..scheduler import AsyncScheduler
from .scraper import Scraper, ScrapeException
from .database import MetricDAO, initialize_db

# Blueprint Endpoints
from .api import api
from .discovery import discovery



def create_server(config_path: str):

    async def setup_server(app: Sanic, loop: asyncio.AbstractEventLoop):
        """ Main entrypoint, creates all coroutines and returns """
        config.load_config(app, config_path)  # @TODO
        await initialize_db(app)

        # @TODO improve!
        s = AsyncScheduler(loop=loop)
        for target in app.fireplace.targets:
            s.schedule_every(app.fireplace.scrape_interval,
                             Scraper.get_handler(app, target))
    
    app = Sanic("fireplace_server")

    @app.route("/")
    async def index(request):
        return await file(os.path.join(os.path.dirname(__file__), 'views/index.html'))

    @app.route("/main.js")
    async def main_js(request):
        return await file(os.path.join(os.path.dirname(__file__), 'views/main.js'))

    app.register_blueprint(api)
    app.register_blueprint(discovery)
    app.register_blueprint(swagger_blueprint)

    # Startup handler for fireplace server
    app.register_listener(setup_server, "before_server_start")

    return app
