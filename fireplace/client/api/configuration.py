from sanic.response import json
from sanic_openapi import doc
from . import api
from ...helper.api import query_arg


@api.route("/reconfigure")
@doc.description("Reconfigure the maximum temperature and measurement interval")
@doc.response(200, None, description="Reconfiguration successful")
@doc.response(400, None, description="Invalid request")
@query_arg("threshold", float, description="New temperature Threshold")
# @TODO adapt AsyncScheduler
# @query_arg("every", float, description="New measurement interval")
async def reconfigure(request, threshold: float):  #, every: float):
    request.app.fireplace.threshold = threshold
    # request.app.fireplace.every = every
    return json({})


@api.route("/config")
@doc.description("Query the current configuration")
@doc.response(200, None, description="Current configuration")
async def config(request):
    return json(request.app.fireplace)