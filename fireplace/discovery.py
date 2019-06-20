from sanic import Blueprint
from sanic.response import json

bp = Blueprint("discovery")

@bp.route("/")
def discover(request):
    return json({
        "scrape_interval": 11.0,
        "max": 20.0,
    })