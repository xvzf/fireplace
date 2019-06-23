import logging
import asyncio
from typing import Coroutine, Awaitable, List

logger = logging.getLogger(__name__)


class AsyncScheduler:
    """ Async Scheduler """

    # Holds all scheduled coroutine runners so we can tear them down correctly
    tasks: List[Coroutine]
    # Holds the eventloop
    loop: asyncio.AbstractEventLoop

    def __init__(self, loop: asyncio.AbstractEventLoop = None):
        self.loop = loop or asyncio.get_event_loop()
        self.tasks = []

    def schedule_every(self, seconds: float, to_schedule: Awaitable):
        """ Schedules a coroutine 

        :param seconds: Number of seconds to sleep between tasks; float
        :param to_schedule: Coroutine generator to schedule
        """
        # @TODO possibly leaking coroutines
        async def dispatch():
            while True:
                task = self.loop.create_task(to_schedule())
                await asyncio.sleep(seconds)
                #  @TODO maybe gracefully shut this down? :)
                if not task.done():
                    task.cancel()
                    logger.warning(
                        "Scheduled coroutine {task} did not exit in time, canceled")

        # Add coroutine scheduler
        task = self.loop.create_task(dispatch())
        self.tasks.append(task)
        logger.info(f"scheduled coroutine {task} every {seconds}s")

    def teardown(self):
        """ Clear all running tasks """
        # Iterate through all created scheduler tasks and cancel them if they
        # did not already finish (which should not happen)
        for t in self.tasks:
            if not t.done():
                t.cancel()
            else:
                logger.error("Scheduler coroutine exited, should never happen")
        self.tasks = []
