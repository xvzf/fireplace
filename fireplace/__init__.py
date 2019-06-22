import logging
import asyncpg
from sanic import Sanic
from sanic_openapi import swagger_blueprint

# Set debug level for now
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Blueprint Endpoints
from .api import api
from .discovery import discovery

# Fireplace related setup routines
from .fireplace import setup_server


def create_server():
    app = Sanic("fireplace_server")
    app.register_blueprint(api)
    app.register_blueprint(discovery)
    app.register_blueprint(swagger_blueprint)

    # Startup handler for fireplace server
    app.register_listener(setup_server, "before_server_start")

    return app