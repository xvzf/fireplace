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
    async def add_many(db: asyncpg.pool.Pool, metrics: List[Metric]) -> bool:
        """ Adds many metrics to the database """
        async with db.acquire() as conn:
            logger.debug(await conn.copy_records_to_table(
                "metrics",
                records=[(m.time, m.name, m.temperature) for m in metrics])
            )
            return True
        return False

    @staticmethod
    @mapper(Metric)
    async def get_current(name: str) -> List[Metric]:
        """ Queries the current temperature of a sensor """
        return "select * from metrics where name = $1 order by time desc limit 1", name

    @staticmethod
    @mapper(Statistics)
    async def get_stats(name: str, interval_seconds: int, offset_seconds: int, limit: int):
        """ Wrapper around the time_bucket operation """
        return (
            """
            select _time as time, min_temperature, max_temperature, avg_temperature from (
                select
                    time_bucket($2 * interval '1 second', time) as _time
                    , min(temperature) as min_temperature
                    , max(temperature) as max_temperature
                    , avg(temperature) as avg_temperature
                from
                    metrics
                where
                    name = $1
                group by _time
                order by _time desc
                limit $3
            ) as aggregated
            order by time asc
            """,
            name,
            interval_seconds,
            limit
        )
