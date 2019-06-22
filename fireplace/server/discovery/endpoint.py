from sanic.response import json
from sanic_openapi import doc
from . import discovery
from .containers import Target
from .. import config
from ...helper.json import dumps


@discovery.route("/<target>")
@doc.summary("Transmit configuration settings for targets")
@doc.response(200, Target, description="Target configuration parameters")
@doc.response(404, None, description="Target is not configured")
def get_discovery(request, target: str):
    for t in request.app.fireplace.targets:
        if target == t.name:
            return json(t)
    return json(None, status=404, dumps=dumps)
