from sanic import Blueprint
from sanic.response import json

api_v1 = Blueprint("api_v1", url_prefix="/api", version="v1", strict_slashes=True)
api = Blueprint.group(api_v1)

from . import query