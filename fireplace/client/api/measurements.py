from datetime import datetime
from sanic.response import json
from sanic_openapi import doc
from . import api
from . import containers
from ...helper.api import query_arg
from ...helper.json import dumps


@api.route("/temperature")
@doc.description("Query endpoint for temperature measurements")
@doc.response(200, [containers.Measurement], description="Sensor values starting from the requested timepoint")
@doc.response(400, None, description="Invalid query parameter")
@query_arg(
    "from_time",
    datetime.fromisoformat,
    description="Only measurements starting from the given timepoint")
async def temperature(request, from_time: datetime):
    return json(request.app.buffer.get_from(from_time), dumps=dumps)
