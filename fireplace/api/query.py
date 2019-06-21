from sanic.response import json, text
from sanic_openapi import doc
from typing import List
from datetime import datetime
from .containers import Metric as MetricAPI, Statistics as StatisticsAPI
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
@doc.consumes({
    "timeframe": doc.String("Timeframe in which data should be analysed, max 2678400 (1 month)")
})
@doc.response(200, StatisticsAPI, description="Target statistics")
@doc.response(404, None, description="Sensor was not scraped yet / does not exist")
async def get_statistics(request, target: str):
    timeframe = 3600
    try:
        arg_timeframe = int(request.args.get("timeframe", 3600))
        timeframe = arg_timeframe if arg_timeframe <= 2678400 else timeframe
    except:
        logger.warning(f"Wrong query parameter for statistics: {request.args.get('timeframe')}")
    
    tmp: List[Statistics] = await MetricDAO.get_stats(  # pylint: disable-msg=too-many-function-args
        request.app.db,
        target,
        int(timeframe),
        datetime.now()
    )

    return json(tmp[0]) if tmp else json(None, status=404)