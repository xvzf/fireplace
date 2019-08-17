import time
import http3
from dataclasses import dataclass
from typing import List
from datetime import datetime
from .helper.json import dumps, convert_to_basic
from . import logger


@dataclass
class Target:
    """ target config store """
    url: str
    threshold: float
    name: str
    every: float
    alert_interval: float
    alert_targets: List[str]

    # For internal use only
    last_temp_alert: float = None
    last_unavail_alert: float = None

    async def temp_alert(self, temp: float):
        """ Provides functionality like lodash in JS """
        if self.last_temp_alert:
            diff = float(time.time() - self.last_temp_alert)
            if diff <= self.alert_interval:
                self.last_temp_alert = time.time()
                return

        self.last_temp_alert = time.time()
        await self._send_alert({
            "sensor": self.name,
            "event": "max_temp_exceeded",
            "threshold": self.threshold,
            "measured_temp": temp,
            "timestamp": datetime.now()
        })

    async def unreachable_alert(self):
        """ Provides functionality like lodash in JS """
        if self.last_unavail_alert:
            diff = float(time.time() - self.last_unavail_alert)
            if diff <= self.alert_interval:
                self.last_unavail_alert = time.time()
                return

        self.last_unavail_alert = time.time()
        await self._send_alert({
            "sensor": self.name,
            "event": "unreachable",
            "timestamp": datetime.now()
        })

    async def _send_alert(self, data: dict):
        """ Actually sends the post request to the sepcified targets """
        logger.warning(f"Sending alert for sensor {self.name}, {dumps(data)}")
        async with http3.AsyncClient() as client:
            for target in self.alert_targets:
                try:
                    await client.post(target, json=convert_to_basic(data))
                except:
                    logger.error(f"Could not POST alert to {target}")