from sanic import Blueprint

api = Blueprint("api")

from . import measurements
from . import configuration