import http3
import pytz
from ujson import loads
from sanic import Sanic
from datetime import datetime
from .database import MetricDAO, Metric
from .import config
from .. import logger


class ScrapeException(Exception):
    pass


class Scraper:

    @staticmethod
    def get_handler(app: Sanic, target: config.Target):
        """ Generats the async scrape function which handles *EVERYTHING* """

        async def scrape():
            try:
                last_db = await MetricDAO.get_current(app.db, target.name)  # pylint: disable-msg=too-many-function-args
                # Extract latest scrape time
                last_scraped = last_db[0].time if last_db else datetime.fromtimestamp(
                    0).replace(tzinfo=pytz.utc)
                metrics = await Scraper.read_sensor(target, last_scraped)

                # Add retrieved values to database
                await MetricDAO.add_many(app.db, metrics)

                max_temp = max([metric.temperature for metric in metrics])
                if max_temp > target.threshold:
                    await target.temp_alert(max_temp)

            except ScrapeException as e:
                logger.warning(f"Could not retrieve data from {target}")
                await target.unreachable_alert()
            except Exception as e:
                logger.exception(e)

        return scrape

    @staticmethod
    async def read_sensor(target: config.Target, last_scraped: datetime) -> Metric:
        """ Retrieve sensor data from a target (IPv4, IPv6 or DNS)

        :param target: Target address
        :returns: {temperature: ...}
        """
        async with http3.AsyncClient() as client:
            try:
                resp = await client.get(target.url, params={
                    "from_time": last_scraped.isoformat()
                })
                if resp.status_code != 200:
                    raise ScrapeException
                return [Metric(
                    name=target.name,
                    time=datetime.fromisoformat(
                        i["time"]).replace(tzinfo=pytz.utc),
                    temperature=i["temperature"]
                ) for i in loads(resp.text)]
            except ConnectionRefusedError:
                raise ScrapeException
