from sanic.response import json, text
from sanic_openapi import doc
from typing import List
from datetime import datetime
from .containers import Metric as MetricAPI, Statistics as StatisticsAPI
from .helper import query_arg
from . import api_v1
from .. import logger
from ..database import(
    MetricDAO,
    Metric,
    Statistics
)


@api_v1.route("/current/<target>")
@doc.summary("Last data from target (based on config name)")
@doc.response(200, MetricAPI, description="Latest metric received from the sensor")
@doc.response(404, None, description="Sensor was not scraped yet / does not exist")
async def get_current_temp(request, target):
    tmp: List[Metric] = await MetricDAO.get_current(  # pylint: disable-msg=too-many-function-args
        request.app.db,
        target
    )

    return json(tmp[0]) if tmp else json(None, status=404)


@api_v1.route("/stats/<target>")
@doc.summary("Statistics (min, max, avg) from a targed (based on config name and interval in seconds)")
@doc.response(200, StatisticsAPI, description="Target statistics")
@doc.response(404, None, description="Sensor was not scraped yet / does not exist")
@query_arg("offset", int, description="Time offset in seconds")
@query_arg("interval", int, description="Interval in seconds")
@query_arg("latest", int, description="Get the latest n data points")
async def get_stats(request, target: str, interval: int, offset: int, latest: int):

    tmp: List[Statistics] = await MetricDAO.get_stats(  # pylint: disable-msg=redundant-keyword-arg
        request.app.db,
        name=target,
        interval_seconds=interval,
        offset_seconds=offset,
        limit=latest
    )

    return json(tmp) if tmp else json(None, status=404)