import asyncpg
from dataclasses import dataclass
from functools import wraps
from .. import logger


def mapper(Target: dataclass):
    """ Maps SQL queries to dataclasses """
    def decorator(query):

        @wraps(query)
        async def wrapper(db: asyncpg.pool.Pool, *args, **kwargs) -> dataclass:
            async with db.acquire() as conn:
                sql_args = await query(*args, **kwargs)
                logger.debug(f"Running query: {sql_args}")
                records = await conn.fetch(*sql_args)
                return [Target(**dict(r)) for r in records]
            # @TODO Error handling
            return None
        return wrapper

    return decorator