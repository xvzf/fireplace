import asyncio
import random
from datetime import datetime
from sanic import Sanic
from sanic.response import json
from sanic_openapi import swagger_blueprint
from .. import logger
from ..scheduler import AsyncScheduler
from .datastore import MeasurementBuffer, Measurement
from . import discover
from .sensor import Sensor
from .api import api


async def setup_client(app: Sanic, loop: asyncio.AbstractEventLoop):

    async def measure():
        val = await Sensor.read()
        app.buffer.add(Measurement(
            time=datetime.now(),
            temperature=val
        ))

    app.fireplace = await discover.get_config(app.config["discovery_url"])

    app.buffer = MeasurementBuffer()

    s = AsyncScheduler(loop=app.loop)
    s.schedule_every(app.fireplace.every, measure)


def create_client(name: str, server: str):
    """ Dummy server for now """

    app = Sanic("fireplace_client")
    app.config["discovery_url"] = server
    app.blueprint(api)
    app.blueprint(swagger_blueprint)

    app.register_listener(setup_client, "before_server_start")

    return app
