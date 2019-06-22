from sanic import Blueprint

api = Blueprint("api", strict_slashes=True)

from . import measurements
from . import configuration