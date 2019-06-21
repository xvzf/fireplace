import asyncpg
from datetime import datetime
from typing import List
from .containers import Metric, Statistics
from .mapper import mapper
from .. import logger


class MetricDAO:
    """ Data access class """
    @staticmethod
    @mapper(Metric)
    async def get_all() -> List[Metric]:
        return "select * from metrics"

    @staticmethod
    async def add_now(db: asyncpg.pool.Pool, name: str, temperature: float) -> bool:
        """ Adds value to timeseries with the current timestamp """
        async with db.acquire() as conn:
            logger.debug(await conn.execute(
                "insert into metrics (time, name, temperature) values (TO_TIMESTAMP($1), $2, $3)",
                datetime.timestamp(datetime.now()),
                name,
                temperature
            ))
        # @TODO
        return True

    @staticmethod
    @mapper(Metric)
    async def get_current(name: str) -> List[Metric]:
        """ Queries the current temperature of a sensor """
        return "select * from metrics where name = $1 order by time desc limit 1", name

    @staticmethod
    @mapper(Statistics)
    async def get_stats(name: str, timeframe: int, start_time: datetime) -> List[Statistics]:
        """ Queries target statistics """
        return (
            """
            select
                min(temperature) as min_temperature
                , max(temperature) as max_temperature
                , avg(temperature) as avg_temperature
                , count(*) as data_count
            from
                metrics
            where
                name = $1 and
                time between
                    TO_TIMESTAMP($3) - $2 * interval '1 second'
                    and
                    TO_TIMESTAMP($3)
            """,
            name,
            timeframe,
            datetime.timestamp(start_time)
        )