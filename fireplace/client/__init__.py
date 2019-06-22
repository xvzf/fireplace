import random
from sanic import Sanic
from sanic.response import json


def create_client(name: str, server: str):
    """ Dummy server for now """

    app = Sanic("fireplace_client")

    @app.route("/temperature")
    async def get_temperature(request):
        """ Measures temp and returns it in json representation """
        return json({
            "temperature": random.randint(200, 400) / 10.0
        })

    return app
