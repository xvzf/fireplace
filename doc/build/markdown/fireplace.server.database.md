# fireplace.server.database package

## Submodules

## fireplace.server.database.containers module


#### class fireplace.server.database.containers.Metric(time: datetime.datetime, name: str, temperature: float)
Bases: `object`

Metric timepoint

!!! if you change the datatypes of this class, adapt MetricMeta !!!


#### class fireplace.server.database.containers.Statistics(time: datetime.datetime, min_temperature: float, max_temperature: float, avg_temperature: float)
Bases: `object`

Target statistics

## fireplace.server.database.dao module


#### class fireplace.server.database.dao.MetricDAO()
Bases: `object`

Data access class


#### static add_many(db: asyncpg.pool.Pool, metrics: List[fireplace.server.database.containers.Metric])
Adds many metrics to the database


#### static get_all()

#### static get_current(name: str)
Queries the current temperature of a sensor


#### static get_stats(name: str, interval_seconds: int, offset_seconds: int, limit: int)
Wrapper around the time_bucket operation

## fireplace.server.database.mapper module


#### fireplace.server.database.mapper.mapper(Target: dataclasses.dataclass)
Maps SQL queries to dataclasses

## Module contents


#### fireplace.server.database.initialize_db(app: sanic.app.Sanic)
Initialize database connection based on loaded config
