from datetime import datetime
from sanic.response import json
from sanic_openapi import doc
from . import api
from ...helper.api import query_arg


@api.route("/temperature")
@doc.description("Query endpoint for temperature measurements")
@query_arg(
    "from_time",
    datetime.fromisoformat,
    description="Only measurements starting from the given timepoint")
async def temperature(request, from_time: datetime):
    print(len(request.app.buffer.ring))
    return json(request.app.buffer.get_from(from_time))