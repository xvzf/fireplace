import asyncpg
from dataclasses import dataclass
from functools import wraps


def mapper(Target: dataclass, db: asyncpg.pool.Pool):
    """ Maps SQL queries to dataclasses """
    def decorator(query: str):

        @wraps(query)
        async def wrapper(*args, **kwargs) -> dataclass:
            async with db.acquire() as conn:
                records = await conn.fetch(await query())
                return [Target(**dict(r)) for r in records]
            # @TODO Error handling
            return None
        return wrapper

    return decorator