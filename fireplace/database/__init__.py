import asyncpg
from sanic import Sanic
from dataclasses import dataclass
from .containers import *
from .dao import *
from .. import logger


async def initialize_db(app: Sanic):
    """ Initialize database connection based on loaded config """
    app.db = await asyncpg.create_pool(**app.fireplace.database)
    logger.info("Connected to timescaledb/postgresql")
