# fireplace.scheduler package

## Submodules

## fireplace.scheduler.async_scheduler module


#### class fireplace.scheduler.async_scheduler.AsyncScheduler(loop: asyncio.events.AbstractEventLoop = None)
Bases: `object`

Async Scheduler


#### schedule_every(seconds: float, to_schedule: Awaitable[T_co])
Schedules a coroutine

@param seconds: Number of seconds to sleep between tasks; float
@param to_schedule: Coroutine generator to schedule


#### teardown()
Clear all running tasks

## Module contents
