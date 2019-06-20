import asyncpg
from dataclasses import dataclass
from datetime import datetime
from typing import List
from .mapper import mapper
from .containers import Metric
from .. import logger


# Database connection, filled by initializing
db: asyncpg.pool.Pool = None


async def initialize_db(**kwargs):
    """ Initialize database connection based on loaded config """
    global db
    db = await asyncpg.create_pool(**kwargs)
    logger.info("Connected to timescaledb/postgresql")


class MetricDAO:
    """ Data access class """
    @staticmethod
    @mapper(Metric, db)
    async def get_all() -> List[Metric]:
        return "select * from metrics"

    @staticmethod
    async def add_now(name: str, temperature: float) -> bool:
        """ Adds value to timeseries with the current timestamp """
        async with db.acquire() as conn:
            logger.debug(await conn.execute(
                "insert into metrics (time, name, temperature) values ($1, $2, $3)",
                datetime.now(),
                name,
                temperature
            ))
        # @TODO
        return True
